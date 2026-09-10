# Diels–Alder product evidence and an unresolved control assay

The acquired [Siegel et al. 2010 article](https://pmc.ncbi.nlm.nih.gov/articles/PMC3241958/)
connects the named DA_20_10 construct to a two-substrate Diels–Alder reaction,
kinetic parameters, reported catalytic-group mutation effects and separate
product outcomes. It does **not** establish an assay- and parameter-matched
product/control relation within the acquired scope. The supplement remains
unacquired. This is the supported evidence gap, not a claim that mutation
effects or the missing details do not exist.

The [source packet](../data/atlas/study_context/diels_alder_2010/source_qualification.json)
and [computational review](../data/atlas/study_context/diels_alder_2010/source_review.json)
carry the precise boundaries under [CE-033](../CLAIMS.md).

## What can be recovered

The existing consumer and reaction/participant relation work without a runtime
change:

```sh
python scripts/query_atlas_perturbations.py --study diels_alder_2010
python scripts/query_atlas_perturbations.py --comparison diels_alder_2010:qualified-mutant-parameter
```

| Source evidence | Returned scope | Refused transfer |
| --- | --- | --- |
| Table 1 DA_20_10 kcat 2.13 ± 0.24 hr⁻¹; KM-diene 1.3 ± 0.1 mM; KM-dienophile 72.8 ± 5.1 mM | Three parent fitted-parameter records; printed errors are calculated 95% confidence intervals | No mutant rate, pooled KM, unit conversion or recomputed efficiency |
| Main paragraph P9: Q195E 450-fold and Y121F 27-fold activity reductions | Two author-reported comparative assertions on the named DA_20_10 mutation background | No qualified underlying parameter, assay, raw control/mutant values, reciprocal residual rate, significance or residue-importance ranking |
| P11: >80% diene conversion | A strict bound in its high-enzyme context | No isolated yield, product configuration or borrowed stereochemistry-assay conditions |
| P14: >97% source-assigned 3R,4S endo product share | A strict product-distribution bound; chiral LC-MS/MS and Figure 4 context remain separate from the unacquired Figure S8 calculation | No exact 97%, ee, dr, purity, conversion or mutant selectivity |

The five added parameter records comprise three fitted parent parameters and
two reported fold assertions, not five experiments or five measured rates.
The other three printed Table 1 specificity/efficiency columns are intentionally
outside this bounded projection; this is not full-table coverage. Their values
are not declared missing and are not recomputed from the selected columns.
The complete view has 118 parameter records and 56 comparison requests; 41
permit descriptive arithmetic and 15 abstain. All 113 inherited records and
55 inherited comparisons retain their values and scope. The new request
abstains specifically from reconstructing parameter-matched mutant/control
measurements. Its context retains both reported mutation effects.

Product bounds are structured under `evidence_context.da2010` with null central
values, distinct context IDs, explicit comparators and thresholds. They are
not flattened into numeric parameter records or relabeled qualitative traces.
The generic projection preserves the original source records and refuses
arithmetic on the unqualified mutant-effect assay.

## Chemical and experimental identity

Figure 1 names diene 1 as 4-carboxybenzyl trans-1,3-butadiene-1-carbamate and
dienophile 2 as N,N-dimethylacrylamide. Product 4 is the cyclohexene cycloadduct;
3 labels a transition-state/design schematic. The shared product participant
has no stereochemical assignment. Individual product observations own that
assignment. The figure draws carboxylate on the reactant and CO2H on the
product, so the source-named relation supplies no balanced equation, proton
transfer or canonical atom map. Distinct KM parameter markers bind each
source column to its corresponding reactant ID.

The Figure 4 background uses 2 mM diene, 70 mM dienophile and 24 h. Its enzyme
arm uses 50 μM DA_20_10, 0.5 mM diene, 10 mM dienophile and 48 h. Both captions
specify PBS and 298 K; pH is not assigned from the earlier screening assay.
P14's reported 47% uncatalyzed target share has no verified Figure 4 condition
or integration join and cannot supply a matched selectivity effect. No project
peak integration was performed, and the stereochemical reference was not
independently authenticated.

The main text gives DA_20_10's six changes from DA_20_00 and names its Q195E
and Y121F substitutions, but supplies no inspected exact sequences or assay
specimen authentication. DA_20_10 is the named mutation background; the fold
denominator is implied by context rather than an explicitly identified control
measurement.

The article describes 3I1C as apo DA_20_00_A74I. It differs from DA_20_10 by five
additional changes, including A272N, which was proposed to constrain the Tyr
conformation. No coordinates were acquired. This structure cannot establish
final-construct ligand geometry or a structural explanation for the mutation
effects. Mutation sensitivity likewise does not isolate hydrogen bonding,
orbital-energy modulation, desolvation or conformational contributions.

## Acquisition, reuse and the next decision

The distinct `designed-diels-alder-siegel2010` batch consumed 14 requests and
502,726 response-body bytes, including discovery, redirects, failures and the
two figures. Its [receipt](../data/atlas/study_context/diels_alder_2010/acquisition_receipts.json)
preserves cumulative accounting; inherited source budgets are unchanged. The
article and Figures 1/4 are hash-verified in the Git common directory's local
source cache. Publisher bodies and images are not redistributed.

The PMC supplement route returned a challenge page, the publisher returned
403, the public author page supplied no supplement link, and EuropePMC returned
a not-open-access response or mirror error. These results establish access
limits, not supplement contents. Repeating those unchanged routes is stopped.

Two-reactant chemistry, separate substrate parameters and reported effects fit
the same data projection without enzyme-specific code. Reuse is demonstrated
at the named-source relation and its exclusions; the requested complete
product/control join remains unavailable. No curation speedup, superiority to
competent source reading, design success, independent review, project experiment
or evidence-tier promotion is claimed.

Next test the common relation on the existing transketolase E366Q
partner-subunit case, where reporter nondetection and retained turnover belong
different substrates and endpoints. This tests cofactor-dependent reuse and
prevents a generic inactivity label. Stop after one executable relation or a
specific shared-representation gap; a new isolated annotation is insufficient.
Return to the Diels–Alder control-assay join only when a new permitted supplement
witness becomes available.
