# Calmodulin controls qualify lysine-mechanism inference

Raymond et al., *Protein Science* 24:561–570 (2015),
[DOI 10.1002/pro.2622](https://doi.org/10.1002/pro.2622), reports methodol
cleavage by calmodulin derivatives after controls targeting lysine, histidine
and the N-terminal amine. Residual activity in this series therefore does not
uniquely identify a lysine-covalent route. The controls do not establish a
particular alternative mechanism or prove that hydrophobic association is
the sole cause.

The source annotation is
[`nucleophile_controls.json`](../data/atlas/study_context/calmodulin_2015/nucleophile_controls.json),
with its [computational source review](../data/atlas/study_context/calmodulin_2015/source_review.json).
It reuses the existing perturbation consumer:

```sh
python scripts/query_atlas_perturbations.py --study calmodulin_2015
python scripts/query_atlas_perturbations.py --comparison calmodulin_2015:nucleophile-control-context
```

The first query returns five source kinetic parameter records, two descriptive
ratios and one mechanistic context with no scalar comparison requested. The
second resolves the control chain, separate analogue/calcium evidence, source
conflicts and the retained RA61 component evidence. No runtime change is needed.

## Residual activity survives the named controls

| Table I construct | Source-defined scope | kcat/KM (M⁻¹ s⁻¹) |
| --- | --- | ---: |
| CaM | Full-length calmodulin reference | 0.006 ± 0.001 |
| cCaM | C-terminal domain reference | 0.007 ± 0.002 |
| CaMWN | C-terminal K77A/K94R/H107I/K115N/K148L | 0.005 ± 0.001 |
| Ac-CaMWN | CaMWN plus N-terminal acetylation | 0.004 ± 0.002 |
| CaM L105K / AlleyCatR | Full-length introduced-lysine variant | 0.038 ± 0.002 |

Main p564 says the four lysines and only histidine in cCaM were replaced.
Main p568 describes N-terminal acetylation and reports MALDI-TOF confirmation.
The acquired main text does not supply the raw spectrum or exact sequences;
these controls do not prove complete chemical occupancy or the absence of
every possible nucleophile. CaMWN/cCaMWN and Ac-CaMWN/Ac-cCaMWN are retained
source aliases. C-terminal controls are not silently assigned to full-length CaM.

The central-value ratios are CaMWN/cCaM = 0.7143 and L105K/CaM = 6.3333.
The acetylated endpoint remains directly retrievable with its preparation
lineage, but is not put through the consumer's genetic-background ratio
operation: terminal acetylation is a chemical treatment. No duplicate row or
pseudo-unmutated CaMWN reference is created. These numbers do not show
statistical equivalence, isolated component energetics or a shared microscopic
mechanism. The table's F92K row and the seven-mutant screen are outside this
selected control question.

Saturation was not observed, so separate kcat and KM are unavailable. Table I
and Methods give pH 7.5; Methods specifies 25 mM HEPES, 10 mM CaCl2,
100 mM NaCl, 3.5% acetonitrile, 40 µM protein and 50 µM–1.5 mM methodol,
with absorbance at 350 nm and initial-rate fitting. Temperature is unstated.
The source says measurements were in triplicate but does not define the
printed ± statistic. No SD, preparation count or propagated ratio error is
inferred. Figure 5 instead captions pH 7, 20 mM HEPES and 0.1–1.5 mM
methodol. That discrepancy stays unresolved; its points are not refitted or
joined to Table I as an identical assay. HPLC confirmation is source-reported;
the supporting chromatogram is not acquired or independently reprocessed.

## Analogue and calcium controls answer different questions

Figure 8 compares full-length CaM and L105K with a non-turnover diketone
analogue after 24 hours at pH 7 and 10 mM CaCl2. L105K shows a distinct
absorbance band near 360 nm; the source reports no corresponding reaction for
CaM. This supports the authors' covalent-analogue interpretation, while
Figure 1 calls the species an *enamine* and the Results use *imine* and
*iminium*. Exact bond order, protonation, attachment occupancy and a methodol
turnover intermediate remain unassigned. The blue CaMWN plot label is omitted
from the caption; it is not used to extend the defined CaM/L105K comparison.

Figure 7A shows a calcium-dependent methodol response for full-length L105K.
The no-added-calcium arm also contains 50 µM EDTA. A scoped absence of
above-background activity is not a zero rate. This supports allosteric or
conformational dependence without proving direct calcium participation in
bond chemistry. The Results mention F92K/L105K, whereas Figure 7B names
C-terminal L105K; panel B is not relabeled or transferred to unmutated cCaM.
Neither control supplies an additional Table I rate or an exact kinetic ratio.

## Relation to RA61 and the closed stereoselectivity scout

Raymond2015 discussion/reference 24 invokes Lassila2010's RA61 component
analysis. The query resolves that original evidence alongside these controls:
RA61 changes substrate or proposed water-motif residues, while calmodulin
changes named nucleophiles, a terminal amine and calcium conditions. The
reported roughly 500-fold and 2000-fold component interpretations are not
matched scalar contributions or transferable rates. This distinction is the
useful cross-study relation; no pooled ranking or design-performance claim follows.

The inherited RA61 R/S question closed at a primary construct mismatch:
Raymond2015 measures CaM variants, and its R/S-methodol statement concerns
computational docking. Lassila2010 SI Figure S8 remains two qualitative
racemate-model envelopes, not separate R/S rates or a preferred configuration.
Wang2012's primary body was not obtained through the checked routes. This is
a bounded scout result, not an exhaustive claim that RA61 data do not exist.
The [acquisition appendix](../data/atlas/study_context/ra61_2010/stereoselectivity_acquisition_appendix.json)
records seven new requests / 1,259,662 response-body bytes in the same RA61
batch, now 52 requests / 4,495,921 bytes. No source bodies are redistributed.

The observations, source interpretations and analyst inference remain distinct.
This is correlated computational source review, not independent human review,
a project experiment, a complete mechanism or a demonstrated design result.
