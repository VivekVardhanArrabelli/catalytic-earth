# Forward methodol synthesis with product evidence

The retained Obexer2017 supplement reports RA95.5-8F making methodol from
acetone and 6-methoxy-2-naphthaldehyde: **67% conversion after 3 h** and
**60.1% isolated yield**. This is an actual published synthetic-product outcome,
separate from the existing cleavage and catalytic-group perturbation measurements.
It is a source annotation, not a project experiment or a design-success estimate.
[CE-032](../CLAIMS.md) controls the scope.

The [source packet](../data/atlas/study_context/ra95_2017/forward_synthesis.json)
and its [review](../data/atlas/study_context/ra95_2017/forward_synthesis_review.json)
bind the retained [primary supplement](https://media.springernature.com/original/springer-static/esm/art%3A10.1038%2Fnchem.2596/MediaObjects/41557_2017_BFnchem2596_MOESM342_ESM.pdf),
printed/PDF pp9-11, 17 and Figure S12 p29. The main article body remains
unacquired; the optical-rotation reference literature was not independently
rechecked. Publisher bodies and rendered figures remain in the permitted local
cache and are not redistributed.

## Keep the measured endpoints separate

| Evidence | Source-reported result | Supported scope |
| --- | --- | --- |
| RA95.5-8F, HPLC synthesis monitoring | 67% maximum conversion at 3 h | Product-calibrated HPLC; not isolated yield, initial rate or total turnovers |
| Same product after workup/purification | 78.1 micromol, 19.10 mg, 60.1% isolated yield | Printed yield preserved despite the inconsistent starting amount tuple |
| Product chiral HPLC | 4R:4S = 99.2:0.8; S12 prints greater than 98.4% ee for R | Source-labeled composition; the strict ee bound is not replaced with the exact 98.4% arithmetic from rounded ratio parts |
| RA95.5-8 under source-stated same conditions | 0.7% conversion | Precursor comparator, not a matched single-residue effect |
| RA95.5-8 with longer time and more enzyme | 28:72 S:R and 44% ee; qualitatively comparable yields | 1 day and approximately 50-fold enzyme; exact yield and full altered conditions unavailable |
| Separate apparent-equilibrium experiment | Kapp = 1.2 ± 0.1 M^-1; source-calculated maximum yield 71% | A different assay and a source calculation, not measured isolated yield |

The preparative recipe reports 2 M acetone, 2 mM aldehyde, 0.1 micromolar
RA95.5-8F in 25 mM HEPES/100 mM NaCl, pH 7.5, at 29 °C and 600 rpm.
It names a 50 mL reaction in a 100 mL flask. The cleavage assay's 2.7%
acetonitrile is not specified for this synthesis and is not transferred.
Replicate counts and statistical errors for these synthesis outcomes are not
reported in the inspected scope; missing uncertainty is not zero.

The separate equilibrium assay used 0.20 mM aldehyde, 0.2 micromolar enzyme,
0.1-1.0 M acetone and 200 microliters, reaching an apparent composition after
30-160 min. S12 applies its constant to the nominal 2 M acetone production
conditions, outside that stated measurement range. Keep the 71% ceiling as the
author's calculation; no universal constant or catalyst-induced equilibrium
shift is inferred.

## Two source conflicts travel with the outcome

**Starting amount:** 50 mL × 2 mM implies 100 micromol, while the same recipe
prints 130 micromol. The reported 78.1/130 agrees with 60.1% after rounding.
This does not identify which starting quantity is wrong. The relation preserves
all quantities and blocks repaired yields, closed mass balances and amount-based
productivity estimates.

**Retention-time assignment:** Methods p11 assigns R to 6.0 min and S to
7.9 min. Figure S12's labeled standards and caption assign S to 6.0 min and
R to 7.9 min; the black product trace's major peak is near 7.9 min. Neither
assignment is silently corrected. The normalized retention-time-to-configuration
mapping remains null.

The source nevertheless reports an R-major product in both places. Its p17
Methods declare a separate absolute-configuration assignment by comparison
of optical rotation with literature values; p11 reports +56.5° at 27 °C
(c = 1.47, CHCl3). Retain that author assignment and its basis, without claiming
that this project authenticated the standards or reference rotation. NMR and
HRMS provide reported identity support, not independent enantiomer assignment.

The precursor's 44% ee belongs to the longer-time/higher-enzyme comparison.
It must not be attached to its 0.7% same-condition conversion arm. The source
comparison does not isolate an individual catalytic-group contribution to
synthesis, and the existing Table S1 mutant cleavage rows do not supply that
missing synthesis control.

## Reuse through the common relation

```sh
python scripts/query_atlas_perturbations.py --study ra95_2017 --output /tmp/ra95-outcomes.json
```

The [common relation](ATLAS_PERTURBATION_RELATION.md) projects seven parameter
records from these outcomes: two conversions, one isolated yield and four
source-labeled enantiomer ratio components. Product mass/amount, the strict ee
bound, reported optical rotation, assay conditions and both conflicts remain
structured source context. These seven records are not seven experiments.
The 55 existing perturbation/preference comparison requests are unchanged.
No synthetic single-group comparison or cleavage-to-synthesis ratio is invented.

One genuinely missing shared concept required a small generic extension:
`reaction_id` and `reaction_context` now carry named, role-tagged reactants and
product. The same consumer checks source-assay direction and distinguishes the
aldehyde/acetone input combination from methodol product. Older observations
without that source context return null; no legacy reaction map is invented.
The shared product identity is configuration-neutral. The 8F author assignment
and conflicted chromatogram mapping travel with its individual composition row;
the altered precursor row retains its separate caption-only assignment. The
0.7% conversion arm has no assigned configuration. Chemical identities remain source names, without an
invented canonical reaction or atom map.

New parameters and case mappings are data, with reused exact sequence providers
and the same retained source witness. No enzyme-ID runtime branch is needed.
This is bounded computational reuse and prevention of invalid transfers, not a
measured speedup, superiority to competent primary-source reading, prospective
enzyme-design performance, mechanism proof or independent validation.

There were zero new public-source requests or bytes. The existing RA95 batch
remains at 24 requests / 15,353,338 bytes under its cumulative 100-request /
30-MiB ceiling. No frozen kernel, protected registry or exposure record changed.
