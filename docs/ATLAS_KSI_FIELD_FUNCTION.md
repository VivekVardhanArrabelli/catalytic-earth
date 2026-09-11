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
The primary-source followup below now resolves reference 16's own assay,
while preserving the compilation's unresolved individual row provenance.

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

The [original review](../data/atlas/study_context/ksi_2014/source_review.json) binds
the initial annotation; the [primary followup review](../data/atlas/study_context/ksi_1995/source_review.json)
renews the current files and the narrowly corrected acquisition-status wording.
All three reviewers are correlated
computational agents; they do not provide independent human validation.
No protected protein admission, new experiment, complete mechanism, productive
geometry, evidence-tier promotion or prospective enzyme-design performance
is established.

The initial KSI packet used **12 requests / 5,179,007 response-body bytes**, including
failed routes. Three primary witnesses are retained locally by hash; source
bodies are not redistributed. The prior DERA inquiry remains unassessed after
its bounded access stop: the same RA95 batch is now **33 / 17,556,517**, with
the [appendix](../data/atlas/study_context/ra95_2013/dera_acquisition_appendix.json)
preserving its six requests and the unreviewed erratum flag. No mechanism
conclusion follows from inaccessible DERA text.

## Primary kinetics resolve one comparison, not the whole compilation

Kim and Choi's [1995 primary paper](https://europepmc.org/articles/PMC176927)
is Fried2014 reference 16. Its Table 1 and adjacent methods support a
within-study comparison of *P. putida* biotype B WT, Y16F and D40N. The
[primary packet](../data/atlas/study_context/ksi_1995/primary_kinetics.json)
retains this separately from the 2014 compilation:

```sh
python scripts/query_atlas_perturbations.py --study ksi_1995
python scripts/query_atlas_perturbations.py --comparison ksi_1995:D40N:kcat
```

The study query returns six kinetic parameter records and four descriptive
mutant/WT ratios through the unchanged consumer. Each record carries its
source reaction, assay and uncertainty. The query retains compilation-provenance
limits in shared evidence context and beside each comparison.

| Construct | Primary kcat, s⁻¹ | Primary KM, µM | Derived kcat / WT | Derived KM / WT |
| --- | ---: | ---: | ---: | ---: |
| WT | 26,722 ± 231 | 59.3 ± 1.7 | reference | reference |
| Y16F | 13.3 ± 0.6 | 17.1 ± 3.1 | 0.000497717 | 0.288364 |
| D40N | 0.018 ± 0.001 | 13.3 ± 3.7 | 0.000000673602 | 0.224283 |

Table 1 footnote b defines the printed errors as **twice the standard
deviation from five separate determinations**. Figure 4's points instead
average three activity measurements per substrate concentration; these are
not fifteen independent replicates or five protein preparations. The source's
rounded relative-kcat entries, 10⁻³·³ and 10⁻⁶·², remain distinct from the
consumer's central-value quotients. No ratio error or significance is inferred.

All three constructs were assayed at 30 °C in 34 mM potassium phosphate,
pH 7.0, with 2.5 mM EDTA and 3.3% methanol by volume. The substrate series
was 11.6, 34.9, 58.2, 81.5 and 116.4 µM. Product formation and
Lineweaver–Burk regression supplied the kinetic parameters; Figure 4 reports
absorbance change at 248 nm. Some readout details are delegated to the paper's
reference 24, so this is a qualified within-table comparison, not a complete
reconstruction of the assay. The authors report full-gene sequencing of both
mutants with only their intended substitutions. This supports their named
constructs without asserting project-verified physical specimen sequences.

Both mutant **apparent KM values decrease while turnover falls sharply**.
That endpoint pattern does not identify equilibrium affinity, an unchanged
fold, the rate-limiting step or the mechanism of residual activity. The source
authors' tighter-binding interpretation is not adopted as a Kd measurement.
Its Figure 1 reaction context is source-described; it does not newly measure
the stereochemical proton trajectory of each mutant.

The provenance join stops at a concrete mismatch: primary WT/Y16F values
and errors differ from the 2014 entries, 24,300 ± 3,400 and 12 ± 2.
D40N matches the displayed 0.018 ± 0.001 pair, and the 2014 main prose cites
reference 16 for its impairment. This supports a candidate lineage, without
an explicit row-level attribution or a second independent measurement.
It does not justify copying 1995 conditions or the two-SD error model onto
the compiled rows. Both tables imply about 2,000-fold Y16F turnover loss;
the scope of Fried2014's approximate 10⁴ prose remains unresolved.

Kim1995 explicitly relates *P. putida* Asp40/Tyr16 to *C. testosteroni*
Asp38/Tyr14. Homolog correspondence does not establish D40N solution-hydroxide
catalysis or reketonization limitation. The exact Xue1991 reference cited for
that mechanism remained unavailable at primary-body depth after a bounded
identifier check; its truncated abstract is not used to fill those premises.

The [same-batch acquisition appendix](../data/atlas/study_context/ksi_1995/acquisition_receipts.json)
continues the KSI total to **18 requests / 5,441,734 response-body bytes**,
including the redirects and failed mechanism-paper route. The useful addition
is a qualified primary kinetic relation plus a prevented cross-study method
transfer. Source selection and interpretation remain manual; no measured
curation-time saving, complete mechanistic chain or design performance follows.
