# AHAS II populations and source net rates

One source-named E. coli AHAS II Met250Ala construct connects overall turnover
to donor-adduct formation, decarboxylation, carboligation and product liberation.
These are the source's **forward-net constants**, inferred from steady-state
acid-quench NMR populations and turnover. They are not direct measurements of
individual microscopic forward rates (CE-046).

```sh
python scripts/query_atlas_perturbations.py --model-link ahas_2005:Met250Ala:pyruvate_net_transit
```

The [primary paper](https://europepmc.org/articles/PMC545553) reports this
single Met250Ala / Pyr + Pyr row in Table 2 (printed p556, PDF p4):

| Source quantity | Value, s^-1 | Scope in the source model |
| --- | ---: | --- |
| kcat | 3 ± 0.1 | Overall turnover input, per source-assumed active site |
| k′2 | 28 ± 7 | Net lactyl-ThDP formation from bound donor pyruvate |
| k′3 | 35 ± 7 | Net decarboxylation of lactyl-ThDP |
| k′4 | 11.1 ± 1.3 | Net carboligation with the second pyruvate |
| k′5 | 5.6 ± 0.3 | Net acetolactate liberation from the product adduct |

The common consumer returns one turnover parameter and four source-inferred
parameter records, with no mutant/WT ratio. They describe one source table row,
not five independent experiments. The WT rows in this table come from an earlier
publication and are outside this increment. Table 1's separate Met250Ala kcat
of 3.03 is not substituted for the selected Table 2 value.

## What was observed, and what was inferred

At 37 °C with 100 mM pyruvate in 0.1 M potassium phosphate, pH 7.6, the source
combines turnover with relative amounts of acid-quenched ThDP derivatives.
Both substrate instances are pyruvate: one is the model's donor and the second
is its acceptor. One 100 mM pool supplies both; their sequential chemical roles
are source-model assignments, not isotope-traced identities.

The turnover component uses an acetoin colorimetric readout for the
acetolactate-forming reaction, with the full analytical protocol delegated to
cited methods. Normalization assumes two sites in a 138-kDa heterotetramer.
NMR instead measures the protein-free acid-quench solution. The source
reconstitutes a 15 mg/mL enzyme solution with 250 µM FAD, 10 mM Mg2+ and
active-site-equimolar ThDP before mixing. These are not asserted as final
reaction concentrations. The two methods are distinct mixtures; whether they
used the same purified protein batch is unestablished.

The reported N-terminal hexahistidine fusion is on the large catalytic subunit
of the source E. coli ilvG2096-derived AHAS II. No complete assayed sequence,
preparation identifier or source-matched mutant structure is supplied here.
The common query therefore uses source-named construct identity.

Equations 2–9 use Cleland's transit-time model under steady state and substrate
saturation. The authors correct unsubstituted ThDP for pyruvate nonsaturation
using Michaelis–Menten; 100 mM must not be treated as verified full saturation
(Table 1 reports apparent KM 36 mM for His-Met250Ala). The Met250Ala spectrum
and peak fractions are explicitly **data not shown**. The source says ALThDP
is most populated with pyruvate alone and interprets liberation as partly rate
determining. No numerical occupancy is reconstructed.

Keep the printed errors without an SD/SEM assignment. The source describes
integration-derived rate-constant errors but does not identify replicate counts
or raw fractions for this row; the origin of the separately measured kcat error
is left unresolved. The reciprocal sum of the rounded net constants yields
3.00348 s^-1, consistent with the printed kcat. This is dependent model/transcription
consistency, not independent experimental confirmation.

## Why a net stage is not an elementary forward arrow

The Discussion (printed pp557–558) states that each quenched species can pool
enzyme forms with and without noncovalently associated substrates or products.
A forward-net constant includes the fraction committed to product rather than
reversal. The authors explicitly allow a lower k′4 to reflect either bond making
or a later k′5 effect. Their expanded equation 10 separates product-adduct
cleavage from product diffusion, either of which can affect k′5.

The source model retains an unparameterized donor-binding equilibrium K1.
k′2 is not K1, kon or a native-pyruvate dissociation constant. The underlying
carboligation and liberation steps remain reversible in the source;
decarboxylation is described as presumably irreversible. Donor-adduct reverse
kinetics remain unestablished. The minimal carboligation stage also collapses
the reversible acceptor-binding step described in equation 10; k′4 is not an
acceptor-binding rate. Neither the minimal
cycle nor its rates establish complete proton/electron states or graph replay.
Figures 5 and 6 are a yeast-based hypothetical arrangement and a WT/2-ketobutyrate
proposal, respectively; they do not provide a Met250Ala/Pyr + Pyr structure.

The [data packet](../data/atlas/study_context/ahas_2005/source_qualification.json)
and [model relation](../data/atlas/study_context/ahas_2005/model_context.json)
place all five quantities at the inference-model level. Each net quantity names
its affected stage; every individual forward/reverse rate slot remains
unassigned. A generic population-inference contract enforces this distinction
and retains the existing TKT, POX and RA61 model outputs. It does not fit new
rates, recover hidden populations or validate the source's kinetic assumptions.

## Acquisition boundary and reusable value

The inherited Steinmetz2010 inquiry stops at the inspected primary abstract:
it reports donor-acylphosphonate binding separately from acceptor specificity,
but its main text and detailed native-donor phase remain unassessed. It does not
show an absence of discriminating experiments. Its reference 8 identified the
Tittmann2005 paper; no construct, analogue or parameter is transferred between
the publications. The [acquisition appendix](../data/atlas/study_context/ahas_2005/acquisition_appendix.json)
carries the existing bibliography batch to 33 requests / 22,997,768 response-body
bytes. Bodies stay in the Git-common cache and are not redistributed.

This increment adds a useful source-model distinction between the donor stage,
other chemical stages and overall turnover. It introduces one shared inference
concept, with chemical facts in data and no enzyme-specific runtime branch.
Manual interpretation and source declarations remain; no measured curation-time
saving, broad chemical coverage or design performance is established. Further
work should test consequential cross-substrate or branching relations, rather
than treating these dependent constants as validated elementary design targets.
