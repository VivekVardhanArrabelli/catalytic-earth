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
At the original source-relation increment, the complete view had 118 parameter
records and 56 comparison requests; 41 permitted descriptive arithmetic and
15 abstained. All 113 inherited records and
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

## The reactive core replays; stereochemical selection remains source-only

The [partial drawing relation](../data/atlas/study_context/diels_alder_2010/reactive_core.json)
connects the existing named reaction to an executable six-carbon constitutional
projection. The same query shown above returns it under
`reactions["diels_alder_2010:diene1-dienophile2-cycloaddition"].connectivity_relations`.
The existing graph-edit engine performs the replay; no separate reaction engine,
new CLI or enzyme-specific runtime rule is introduced.

All six locators are **project-declared**, supported by Figure 1 and the two
omitted substituent anchors. `d1` is the diene carbon directly attached to
carbamate N; `d2`, `d3`, `d4` follow its conjugated chain toward the free terminus.
`a` is the dienophile alkene carbon attached to the amide carbonyl C, and `b`
is its other alkene carbon. Product 4 has the ring
`d1-d2=d3-d4-b-a-d1`.

| Source-drawing edge | Reactants | Product |
| --- | --- | --- |
| d1-d2 | Double | Single |
| d2-d3 | Single | Double |
| d3-d4 | Double | Single |
| a-b | Double | Single |
| d1-a | Absent | Single |
| d4-b | Absent | Single |

Thus two new C-C bonds and four bond-order changes reproduce the declared
product core. Omitting any of these six edits fails replay. The bare carbon
subgraph is symmetric without its boundary groups: replay does not prove map
uniqueness or recover regioselectivity by itself. The preserved carbamate-N
and amide-carbonyl anchors and exact source review supply the interpretation.
A coherently invented wrong after graph can still pass literal replay; it
cannot enter the reviewed query without changing the source-bound provider.

The combined question of mapping this core to atom-specific `3R,4S` stops at
the stereochemical boundary. Figure 1 leaves product 4 unwedged. Figure 4
labels Exo-Re/Exo-Si/Endo-Si/Endo-Re products `3S,4S`/`3R,4R`/`3S,4R`/`3R,4S`,
but its caption does not define `R1`/`R2` or join source locants to our atom IDs.
All four shown products share the selected constitutional core. P14's
`3R,4S endo` assignment and Figure 4's `Endo-Re` label remain opaque source
product metadata, with no computed target selection or atom-level CIP assignment.
The known source-named trans diene is retained outside this graph API, which
does not represent double-bond geometry. Null graph stereo means outside this
projection, not an achiral product or discarded source information.

This projection omits the carbamate, benzyl/carboxyl and amide substituents and
all hydrogens. The remote carboxylate/CO2H discrepancy is still unresolved;
the original reaction's full `atom_map`, balanced equation and proton-transfer
fields remain null. The replay checks literal bonds, not complete valence,
radical state, electron-flow arrows, concertedness, stereochemical authentication,
an observed trajectory or productive geometry. The graph API's `source_flow_id`
contains an explicit project-difference compatibility token, not an invented
source arrow. Existing assay, mutant, construct and evidence-tier limits remain.

The bounded reusable gain is a source-bound connectivity relation alongside
the existing functional and product contexts, with unsupported stereochemical
selection explicit. It adds no canonical reaction, mechanism admission,
experiment or validated design capability. Curation and source review still
require manual effort; no measured speedup or incumbent-superiority claim follows.

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

The Diels-Alder stereo question could be reopened by qualifying the analytical
reference cited in P14 and listed in article R14:
Cannizzaro et al., JACS 2003, 125:2489, doi:10.1021/ja020879d. Only this citation
identity and its source-declared method association have been inspected here;
the cited paper's contents remain unacquired and unassessed. That question is
whether it supplies exact product structures and an assignment basis that can
resolve the opaque stereo labels. Stop at one supported identity/method relation
or an unavailable/conflicting source. A method reference cannot substitute for
Siegel2010's unacquired Figure S8 sample/integration data or establish matched
enzyme/background conditions. Such work would continue the same Siegel source
batch; unchanged blocked supplement routes stay closed. The current program
priority is the distinct reaction-state/deposit join in the marked handoff,
where retained chemical evidence can test a stronger cross-object relation.
