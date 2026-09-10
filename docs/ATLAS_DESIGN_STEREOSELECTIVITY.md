# RA95 activity and substrate preference are separate design endpoints

The 2013 RA95.0 construct favors cleavage of S-methodol, while the selected
evolved RA95.5-8 favors R-methodol. Higher activity does not establish
preservation of the intended substrate preference. This is a source-scoped
interpretation of published enantiopure kinetics, not a new experiment or a
prospective design-success estimate (CE-028).

The post-RA95.5 directed-evolution rounds described in the 2013 study screened
racemic methodol in cell lysates. RA95.5-5 and RA95.5-8 were then characterized
with separate enantiomers using purified protein and UV-vis kinetics.
Screening activity and the intended substrate
preference therefore need separate dataset fields. This association does not
show that racemic screening caused the preference reversal.

The [additive comparison](../data/atlas/study_context/ra95_2013/stereoselectivity.json)
contains eight R/S kinetic rows from Supplementary Table 1, four printed
selectivity factors, and links to the four exact sequence providers in the
[existing construct record](../data/atlas/study_context/ra95_2013/functional_comparison.json).
It preserves that accepted record and its review unchanged. This adds
stereochemical endpoint coverage, not new proteins or independent experiments.

| 2013 construct | Printed R/S selectivity factor | Quotient of displayed R/S efficiencies | Eligible preference |
| --- | ---: | ---: | --- |
| RA95.0 | 0.43 | 0.459 | S |
| RA95.5 | 3.2 | 4.848 | Unresolved; authors report R |
| RA95.5-5 | 5.4 | 5.529 | R |
| RA95.5-8 | 14 | 14.545 | R |

The table defines the factor as `(kcat/KM)R / (kcat/KM)S`. Its placement on
each construct's racemic row does not make it a racemate-specific quantity.
Printed factors and computed quotients remain separate. The latter use
displayed central values; they are neither corrected factors nor independent
measurements. Exact reconciled factors and ratio uncertainties are unavailable.
Differences are not automatically attributed to rounding.

RA95.5's S row prints kcat = 0.17 s^-1, KM = 560 micromolar, and
kcat/KM = 3.3 M^-1 s^-1. Dividing the first two gives approximately 303.57,
which conflicts with 3.3 and can reverse the inferred preference. Its printed
factor 3.2 also differs from 16/3.3. Preserve all these values and the author's
R-preference statement; withhold a reconciled kinetic triplet and integrated
preference label. The original-to-final comparison does not depend on this row.

These are separate enantiopure UV-vis cleavage assays at 29 C in 25 mM HEPES,
100 mM NaCl, pH 7.5, with 2.7% acetonitrile. The source subtracts a matched
buffer-catalyzed background and fits Michaelis-Menten parameters. Printed errors
are SD from two to three independent protein batches; exact row-specific n
and uncertainties for unmarked values remain unknown. KM is not treated as an
equilibrium binding affinity. Source R/S labels do not supply a project-derived
stereochemical graph or an exact enantiomeric excess.

The author design-intent statement names S-methodol, but the 2013 RA95.0 clone
differs by five surface substitutions from the earlier same-named design.
The existing sequence records bind the 2013 study's named constructs; they
do not verify individual assay specimens or the exact earlier design sequence.
The separate racemic lysine-mutant assays cannot assign the enantiomer preference
to Lys83, Lys210, or any single mutation. Cleavage preference also does not
establish selectivity, yield or product enantiomeric excess in reverse synthesis.

The [computational review](../data/atlas/study_context/ra95_2013/stereoselectivity_review.json)
binds the accepted data and documentation to the retained article XML and SI PDF
for [Giger et al. 2013](https://doi.org/10.1038/nchembio.1276), especially SI
Table 1 (page 2), Figure 1 (page 5), Figure 5 (page 9), and the main article's
design-intent, evolution and UV-vis methods passages. All source bodies remain
locally retained and hash-bound, without redistribution. No new source request
was needed: the original named RA95 batch remains 9 requests / 4,454,733 bytes.

Case facts fit existing construct, substrate, assay, parameter and missingness
concepts. Four sequence providers are reused by hash and exact JSON pointer.
No runtime consumer or new validator is added. The reusable contribution is
the explicit endpoint and eligibility relation for dataset use; no new biology,
measured curation speedup or runtime enforcement is claimed.
