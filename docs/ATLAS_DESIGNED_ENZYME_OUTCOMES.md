# Designed-enzyme outcomes require construct and assay identity

The Giger 2013 RA95 series shows why an activity label must name its parameter.
In the evolved RA95.5-5 background, K210M retains the displayed catalytic
efficiency while its reported turnover parameter falls from 0.048 ± 0.007 to
0.023 ± 0.001 s⁻¹. K83M reduces both parameters. The source supports a
background-dependent sensitivity to K83M/K210M substitution. Direct perturbation
evidence here extends through RA95.5-5; RA95.5-8 site assignment remains
unresolved. A catalytic-site label cannot be propagated by lineage alone
(CE-026). [Primary study](https://pmc.ncbi.nlm.nih.gov/articles/PMC3720730/).

## The useful comparison

These are source-reported kinetic parameter values from the eight explicitly marked
fluorescence rows of Supplementary Table 2. Conditions are racemic methodol,
29 °C, pH 7.5, 25 mM HEPES, 100 mM NaCl and 2.7% acetonitrile. Errors are
standard deviations from two independent measurements; this table does not
identify an independent protein-batch count.

| Background and perturbation | kcat (s⁻¹) | Reported kcat/KM (M⁻¹ s⁻¹) |
| --- | ---: | ---: |
| RA95.5 | 0.0030 ± 0.0004 | 20 |
| RA95.5 K83M | 0.00092 ± 0.00004 | 1.4 |
| RA95.5 K210M | 0.0033 ± 0.0002 | 38 |
| RA95.5 K83M/K210M | 0.0000050 ± 0.0000010 | 0.0070 |
| RA95.5-5 | 0.048 ± 0.007 | 490 |
| RA95.5-5 K83M | 0.00068 ± 0.00002 | 2.3 |
| RA95.5-5 K210M | 0.023 ± 0.001 | 490 |
| RA95.5-5 K83M/K210M | 0.000047 ± 0.000004 | 0.085 |

The engineered K83M/K210M derivatives of the evolved RA95.5 and RA95.5-5
backgrounds retain small positive reported parameter values. These do not
establish a third catalytic residue or another mechanism. The separate
RA95.0-K210M row reports no activity detected above background, without a
numeric detection limit. It stays null, never zero. The first three RA95.0
rows lack the footnote marker that assigns fluorescence conditions and error
semantics to the other rows; their exact method and uncertainty type remain
unresolved. No comparison silently substitutes a main-table parent value.

The table literally prints **M** for KM, while its displayed parameter
arithmetic differs by roughly a factor of one million. The data retain the
literal numbers and unit but leave normalized KM unavailable. A missing micro
prefix is plausible; no correction is established. The efficiency column is
preserved as reported, not recalculated. Ratios of its displayed values imply
neither statistical significance nor equivalence.

## Exact sequence scope

Supplementary Figure 5 supplies four 258-residue sequences, including the
`LEHHHHHH` suffix. Eight perturbation sequences are reconstructed from those
parents and source-declared substitutions; they are explicitly derived strings,
not eight additional sequence observations or verified assay specimens.

The 2013 RA95.0 differs from the earlier same-named construct by five surface
substitutions. The older sequence was not acquired. Within this study, exact
consecutive sequence differences also distinguish Ser53→Thr from the article's
`E53T` description and preserve the later Ser43→Arg reversal. A variant name or
concatenated mutation list cannot replace the sequence.

The data also retain the source-reported design origin in the 1LBL
indole-3-glycerol phosphate synthase scaffold, with eleven active-site changes
and five production/surface changes. This is a bibliographic origin statement;
the exact scaffold sequence and individual substitution effects are unverified.

## Reusable data and limits

The [comparison](../data/atlas/study_context/ra95_2013/functional_comparison.json)
contains four main-table racemic rows and all eleven Supplementary Table 2 rows,
linked to twelve source-defined constructs. These are selected table rows,
not a count of independent experiments or a design-success cohort. The four
main-table rows duplicate the corresponding supplementary entries and are
recorded once, with a separate UV-vis assay identity.

Source-qualified parameters reuse the existing functional-comparison concepts.
Printed and derived sequences, uncertainty, assay method and unit conflicts are
data; no enzyme-specific runtime was added. The contribution is preventing
name-only sequence joins and parameter-blind activity labels. The primary study
already reports the catalytic remodeling; no discovery or measured curation
speedup is claimed.

The [review](../data/atlas/study_context/ra95_2013/functional_review.json) binds
the exact accepted data. The [acquisition record](../data/atlas/study_context/ra95_2013/acquisition_receipts.json)
counts all nine requests and 4,454,733 downloaded response-body bytes in
`designed-retroaldolase-ra95-giger2013`, including failed and challenge responses.
Article XML and the supplementary PDF remain locally retained and hash-bound;
publisher bodies are not redistributed. Exact transcription review requires
matching source bodies.

No explicit fluorescence fitting equation is supplied in the retained source.
The data therefore describe reported parameters; only the UV-vis method has
an explicit Michaelis-Menten fitting model. Mutant activity and the published
parent inhibitor adducts do not isolate chemical participation from structural
effects of substitution. No mutant fold-control, mutant structure or
elementary-step measurement is retained here.

No protein-registry admission, mechanism compilation, evidence-tier promotion,
project experiment or independent human review follows. The published structures
use a covalent diketone inhibitor; they are not reacting-substrate or
transition-state templates. Source inconsistencies in excluded enantiopure/E53A
rows are recorded as unresolved warnings, not silently corrected or used to
support additional claims.
