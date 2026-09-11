# Transketolase mutation effects depend on the measured endpoint

Adding R520Q to the source-named E. coli transketolase TK-1 background gives
TK-2 a lower reported specific activity at 50 mM 3-formylbenzoic acid (3-FBA)
and 50 mM pyruvate, while both have a reported 61% conversion after 24 hours.
The shared query preserves those different endpoints alongside the uncertain
fitted kinetics. It does not assign one overall activity label to the mutation.
This is source annotation under CE-044 and the [truth policy](ATLAS_TRUTH_POLICY.md),
with [claims](../CLAIMS.md) and [errata](../ERRATA.md) controlling interpretation.

The [primary article](https://www.nature.com/articles/s41598-024-51831-z) concerns
E. coli transketolase. The inherited discovery lead therefore closes at a
different enzyme system: it does not resolve the Raj2012 MAL Q73A/L384A
combination. It also supplies no transfer to the existing human TKT2019
F6P/X5P/R5P context.

## One named variant relation, several endpoints

The common 6M background is H100L/H192P/A282P/I365L/D469T/G506A. TK-1 adds
S385Y; TK-2 adds S385Y and R520Q. TK-1 is the engineered comparison reference,
not wild type. Full source mutation sets remain separate from the incremental
R520Q contrast. The source describes C-terminal His6 constructs, but does not
establish an exact assayed sequence. Its pQR791/pQR729 plasmid naming discrepancy
is retained without choosing one identifier.

| Source endpoint | TK-1 | TK-2 | Interpretation boundary |
| --- | ---: | ---: | --- |
| Specific activity at 50 mM 3-FBA, µmol mg⁻¹ min⁻¹ | 20.3 (5) | 8.3 (0.3) | Reported central values and SEM; descriptive TK-2/TK-1 ratio 0.408867 |
| Apparent fitted kcat, s⁻¹ | 134 (85) | 118 (41) | Large SEM; no equality or significance conclusion |
| Apparent KM for 3-FBA, mM | 220 (180) | 530 (190) | Both central estimates exceed the 150 mM tested upper bound |
| Source-labeled conversion at 24 h, % | 61 | 61 | Integer-displayed HPLC peak-area fractions; no uncertainty or equivalence claim |

[Table 3](https://www.nature.com/articles/s41598-024-51831-z/tables/3) supplies
the rates, fit parameters and SEM. Kinetics use 0.1 mg/mL holo-TK, 50 mM
pyruvate, 50 mM Tris–HCl pH 7.0, 2.4 mM ThDP and 9 mM MgCl2 at 21 °C.
Methods state 25–150 mM varied 3-FBA; Results state 0–150 mM. Both end at
150 mM. Raw slopes and fits were not inspected. The source does not establish whether
the specific-activity column is independent of the same fitted curve. Its
central values closely match evaluation of the printed Vm and KM at 50 mM
3-FBA after enzyme-mass normalization; that arithmetic is consistent with
shared fit dependence, not proof of calculation history. These are conditional
two-substrate parameters, not intrinsic elementary-step rates or equilibrium
binding constants.

[Table 2](https://www.nature.com/articles/s41598-024-51831-z/tables/2) gives
the separate conversion protocol at 25 °C, 50 mM of each substrate and 24 h.
Conversion is product peak area divided by combined substrate and product peak
area. Response-factor calibration is not established in the inspected text.
The same 61% values repeated in Table 3 are not additional experiments,
isolated molar yields or evidence for equal time courses.

The article's broad description of R520Q as having “no adverse impact on
activity” cannot replace the specific-activity column. Its intended endpoint
is not made more precise here. The table supports a lower central specific
activity while retaining the distinct fitted and accumulated-product results.
The atlas computes no significance, propagated ratio uncertainty or causal
mechanism. It does not infer a complete mutation square or general donor/acceptor
preference combinability.

## Product, comparator and mechanism boundaries

Scheme 1 names the product as 3-(1-hydroxy-2-oxopropyl)benzoic acid. The authors
report confirmation by LC–MS and NMR for the selected variant conversions;
the supplementary spectra were not inspected. No absolute configuration,
enantioselectivity, isolated yield, complete atom map or balanced canonical
reaction is assigned.

The earlier 6M kinetic values were imported from a different paper, used
0.067 mg/mL enzyme, and varied pyruvate at fixed 50 mM 3-FBA. The current
variants vary 3-FBA at fixed pyruvate. The source's approximately 630-fold
kcat improvement is therefore not a matched kinetic comparison in this query.
The 6M screening conversion also used a different enzyme concentration.

Docking into modeled enamine-ThDP-containing variants remains a computational
interpretation. No pose, reacting geometry, substrate configuration or
microscopic role is attached to the measured contrast. This result does not
validate enzyme design or an elementary mechanism.

## Reuse and evidence

```sh
python scripts/query_atlas_perturbations.py --study tk_2024
python scripts/query_atlas_perturbations.py --comparison tk_2024:R520Q:specific_activity
```

One unchanged consumer resolves the two activity records, two conversion
records, named construct difference, reactant/product relation and source
limitations. Fitted parameters remain contextual evidence, not extra projected
rate comparisons. A generic specific-activity parameter declaration is data;
no enzyme-specific runtime branch is added. The value beyond a table lookup
is a reusable relation that carries the different endpoint and comparator
limits together. Curation still requires source interpretation; no measured
time saving or complete design-enabling mechanism dataset is established.

The [source packet](../data/atlas/study_context/tk_2024/source_qualification.json),
[review](../data/atlas/study_context/tk_2024/source_review.json) and
[acquisition receipts](../data/atlas/study_context/tk_2024/acquisition_receipts.json)
bind the exact publisher article and table HTML. The distinct
`two-substrate-lineages-2024-51831` batch consumed 12 requests and 741,711
response-body bytes, including redirects. Prior batches retain their totals.
Primary bodies remain in the Git-common source cache. Computational source,
representation and adversarial reviews are correlated; they are not independent
human review or project-run experiments.
