# RA95 tyrosine effects depend on the other tyrosine

In the evolved RA95.5-8F background, Y180F has reported catalytic efficiency
33,600 versus parent 33,800 M^-1 s^-1. The Y51F/Y180F double versus Y51F instead gives
170 versus 3,400 M^-1 s^-1. This matched comparison prevents the small
single-mutant efficiency response from becoming a claim that Tyr180 is
independently dispensable.

These are published results from [Obexer et al., Nature Chemistry 9, 50-56
(2017)](https://doi.org/10.1038/nchem.2596), specifically its
[publisher-linked supplement](https://media.springernature.com/original/springer-static/esm/art%3A10.1038%2Fnchem.2596/MediaObjects/41557_2017_BFnchem2596_MOESM342_ESM.pdf).
The full main article remains unacquired and unassessed. All substantive
measurements and sequence statements here are scoped to the supplement.
The [machine-readable annotation](../data/atlas/study_context/ra95_2017/source_qualification.json)
and [source review](../data/atlas/study_context/ra95_2017/source_review.json)
bind exact source bytes, constructs, parameters and limitations.

## The complete paired comparison

Table S1, Figure S11 and Methods page 9 bind the following to (R)-methodol
cleavage, UV/visible detection of naphthaldehyde at 350 nm, 29 C, 25 mM HEPES,
100 mM NaCl, pH 7.5 and 2.7% acetonitrile. These are purified-protein steady-state
parameters, separate from the racemic microfluidic screen and aldol synthesis.

| RA95.5-8F construct | kcat (s^-1) | KM (micromolar) | Printed kcat/KM (M^-1 s^-1) |
| --- | ---: | ---: | ---: |
| Parent | 10.8 ± 0.6 | 320 ± 36 | 33,800 |
| Y51F | 0.12 ± 0.01 | 35 ± 7 | 3,400 |
| Y180F | 2.7 ± 0.1 | 80 ± 11 | 33,600 |
| Y51F/Y180F | (6.3 ± 0.03) × 10^-4 | 3.7 ± 0.1 | 170 |

Errors are the reported standard deviations of two to three independent
measurements; exact n for each row is unspecified. The efficiency column has
no printed uncertainty and remains separate from division of rounded kcat/KM.
Nearly equal printed efficiencies do not establish statistical equivalence.

For each parameter q, define a descriptive multiplicative reference for the
double substitution: **q_expected = q_Y51F × q_Y180F / q_parent**.
This is a declared arithmetic reference, not an experimentally fitted null model.

| Parameter | Multiplicative reference | Reported double | Observed/reference |
| --- | ---: | ---: | ---: |
| kcat (s^-1) | 0.030 | 0.00063 | 0.021, about 48-fold below reference |
| KM (micromolar) | 8.75 | 3.7 | about 0.423 |
| Printed kcat/KM (M^-1 s^-1) | about 3,380 | 170 | about 0.050, about 20-fold below reference |

The complete four-cell comparison supports a departure from multiplicativity
of the displayed central values. It does not supply a significance test,
microscopic coupling energy, isolated chemical cooperation or a proton-transfer
mechanism. kcat and kcat/KM are composite endpoints; substitutions may change
the rate-limiting step, local structure or active fraction. The much lower KM
also explains why the efficiency response differs from the turnover response;
KM is not automatically substrate-binding affinity.

## Other components and controls stay visible

The packet includes all seven Table S1 kinetic rows, including K83M, N110S
and Y51F/N110S/Y180F. Their positive reported kcat values are respectively
4.8 × 10^-5, 0.41 and 1.3 × 10^-5 s^-1. The two missing combinations,
Y51F/N110S and N110S/Y180F, prevent decomposition of a three-way interaction.
No K83-containing combination panel establishes full-tetrad epistasis here.
This is an absence within the acquired panel, not the unacquired main article
or the wider literature.

All seven thermal-shift and seven intact-mass rows are separately typed.
Parent, Y51F, Y180F and double-mutant melting points are 76, 71, 74 and 67 C.
The double's lower melting point is relevant structural evidence. K83M has
a reported melting point of 82 C, above the parent; this constrains gross
thermal destabilization without proving an unchanged active site. The triple's
thermal result is **not determinable because no transition was observed**;
its kinetic result is still a positive fitted value. Thermal assays list buffer
without a stated acetonitrile addition and do not establish active fraction or
local catalytic structure at 29 C. Intact-mass agreement supports the intended
preparations but cannot localize substitutions or authenticate every assay aliquot.

## Exact sequences and structural state limit transfer

Figure S6 directly supplies the 258-residue RA95.5-8F sequence. Six full mutant
strings are explicitly derived from that parent and declared substitutions.
The displayed 2017 RA95.0 and RA95.5-8 strings were independently checked as
identical to the [2013 sequence providers](../data/atlas/study_context/ra95_2013/functional_comparison.json),
which are reused without duplication. This exact sequence relation does not
establish identical assay preparations or conditions across studies.
Figure S6 also has two legacy lineage-label conflicts: it lists E72Y and
T94M for RA95.0 to RA95.5-8, while the exact displayed sequences give F72Y
and T95M. The packet preserves both; all 13 listed changes from RA95.5-8
to 8F agree with those exact strings. RA95.5-8 is a displayed comparison
ancestor of 8F; the final evolution round used shuffled prior templates. Keep the initial methionine and LEHHHHHH suffix
in the printed string: Table S4's mass calculation separately excludes initial
methionine and does not justify shifting residue numbering.

The supplement associates parent structures 5AOU and 5AN7 with unliganded and
covalent diketone-inhibitor states. They were crystallized at different pH values
(4.6 and 7.5), and the inhibitor has reported 75% refined occupancy. No coordinate
files were acquired or remeasured here. Parent structures, author hydrogen-bond
assignments and supporting waters/Ser81 do not prove an exhaustive four-residue
apparatus, a mutant's reacting geometry or microscopic residue roles.

The useful addition is an explicit construct/parameter comparison and its
missing combinations. A competent source reader can reproduce it; no curation
speedup or superiority over incumbent resources is measured. Existing data
concepts and two sequence providers were reused without new runtime code.
This adds no project experiment, protein-registry entry, compiled mechanism,
evidence tier, independent human validation or design-success estimate.
