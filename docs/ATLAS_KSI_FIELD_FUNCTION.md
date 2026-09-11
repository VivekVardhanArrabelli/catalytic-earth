# KSI D40N lies outside the source field–rate model

Fried, Bagchi and Boxer's KSI study joins a physical probe to a functional
comparison: its supporting Table S2 places carbonyl frequencies beside
literature turnover values for six named *Pseudomonas putida* constructs.
The D40N general-base mutant has a large reported turnover impairment with
only a small frequency shift. The authors explicitly exclude it from their
field–rate model because they interpret its mechanism as changed.

The [source annotation](../data/atlas/study_context/ksi_2014/field_function.json)
retains this distinction in the existing perturbation consumer:

```sh
python scripts/query_atlas_perturbations.py --study ksi_2014
python scripts/query_atlas_perturbations.py --comparison ksi_2014:field_function_context
```

The first command returns six measured frequency parameters and six compiled
turnover parameters. The second retains all six constructs on both axes,
together with the source interpretation, model membership and disagreement.
It evaluates no matched-assay ratio or causal field effect.

| Source construct | C=O frequency, cm⁻¹ (SD; n) | Compiled kcat, s⁻¹ (printed ±) | Source field–rate model |
| --- | ---: | ---: | --- |
| WT | 1588.3 ± 2.4; 13 | 24,300 ± 3,400 | Included |
| Y16F | 1647.5 ± 1.3; 7 | 12 ± 2 | Included |
| Y16S | 1621.9 ± 1.3; 8 | 640 ± 60 | Included |
| D103N | 1595.1 ± 0.6; 5 | 5,700 ± 300 | Included |
| D103L | 1624.9 ± 1.6; 7 | 220 ± 10 | Included |
| D40N | 1594.4 ± 0.4; 4 | 0.018 ± 0.001 | Excluded: source-interpreted mechanism change |

Values are from the [author-hosted article and supporting material](https://www.boxerlab.stanford.edu/_files/ugd/4006c9_711c3c14b0484c06bca62b5cbf707a67.pdf),
PDF page 51, printed SI page 44, Table S2. Its spectral footnote defines SD
and independent measurement count; it does not define the statistic or count
for the compiled rate errors. The main text's approximate 10⁴ Y16F activity
loss is not the quotient of the Table S2 kcat entries; these statements are
kept separate rather than repaired.

## What the chemical and experimental join means

The protein probe is **19-nortestosterone sulfate**, not simply the main
text's abbreviated 19-NT and not the turnover substrate. SI Methods D uses
40 mM potassium phosphate in D2O at pD 7.4, approximately 4 mM protein and
3 mM probe, with ligand or isotope editing to separate the carbonyl band
from the protein background. This is a nonreactive product-like bound state,
not a covalent intermediate or an observed turnover event.

The kcat column instead concerns **5-androstene-3,17-dione** and imports
values from references 16, 18 and 19. The source supplies no per-row reference
mapping or full kinetic conditions in this table. The current packet therefore
keeps the kinetic compilation unqualified for a matched-assay comparison.
Source-named variants join the two columns; exact sequences, identical
specimens and cross-study assay equivalence are not established.

SI pages 23–24 state that D40N uses solution hydroxide as base and becomes
limited by reketonization, citing an earlier mechanistic study that this run
has not acquired. That reference's title names **D38N**, whereas the
spectroscopy row is D40N; exact homolog and numbering transfer is unverified.
This is **author interpretation**, not a new mechanistic
experiment or a project-confirmed microscopic assignment. The difference between the printed WT and D40N
frequency means is 6.1 cm⁻¹ by central-value subtraction, with no
propagated error or significance claim; it does not demonstrate an unchanged field.
The useful constraint is that the source's inhibitor-carbonyl field model
does not support a rate prediction for D40N, which it excludes for an
author-interpreted mechanism change. This single case does not characterize
unmeasured base substitutions.

## Measurements, models and disputed attribution

The [primary manuscript](https://pmc.ncbi.nlm.nih.gov/articles/PMC4668018/)
infers signed ensemble-average projected fields of −144 ± 6 MV/cm for WT
and −60 ± 3 MV/cm for Y16F. These are calibration-derived quantities, not
direct field measurements at a reacting transition state. WT lies beyond
the solvent calibration range; SI's quadratic model gives −129 MV/cm,
a 10.4% change from the linear estimate. The solvent calibration also uses
nonsulfated 19-NT in organic solvents and the sulfate in D2O; that chemical
qualification remains attached to the inferred fields.

The reported R² = 0.98 relation includes WT and the four Tyr16/Asp103
mutants. Apparent barriers come from kcat, which combines microscopic steps;
SI acknowledges partially limiting reketonization or product release in WT.
The model assumes transfer from probe to reacting carbonyl and equal fields
in substrate and transition state. The query retains the source model and
its excluded construct; it does not fit a new regression or infer barriers.

The original 70% electrostatic attribution depends on a zero-field
extrapolation and chosen reference reaction. A
[technical comment](https://pmc.ncbi.nlm.nih.gov/articles/PMC4797066/)
argues that accounting for aqueous electrostatics changes the estimate to
about 31.4%, using its own thermodynamic assumptions. The linked author
response was not obtained. Both interpretations remain source-attributed;
neither percentage is an atlas-endorsed causal fraction or a design rule.
This dispute does not erase the observed spectra or the compiled rate table.

## Reuse and limits

Two data panels, source-named construct links and the existing context
operation expose a new physical evidence axis without changing runtime or
forcing signed fields into an unsigned measurement. Signed fields stay in
their derived source context. The gain is a retrievable association between
probe chemistry, a functional compilation and an explicit mechanism-dependent
model exclusion. This is grounded curation, not a novel experimental finding
or measured superiority over a competent literature workflow.

The [review](../data/atlas/study_context/ksi_2014/source_review.json) binds
source objections and exact accepted files. All three reviewers are correlated
computational agents; they do not provide independent human validation.
No protected protein admission, new experiment, complete mechanism, productive
geometry, evidence-tier promotion or prospective enzyme-design performance
is established.

The KSI batch uses **12 requests / 5,179,007 response-body bytes**, including
failed routes. Three primary witnesses are retained locally by hash; source
bodies are not redistributed. The prior DERA inquiry remains unassessed after
its bounded access stop: the same RA95 batch is now **33 / 17,556,517**, with
the [appendix](../data/atlas/study_context/ra95_2013/dera_acquisition_appendix.json)
preserving its six requests and the unreviewed erratum flag. No mechanism
conclusion follows from inaccessible DERA text.
