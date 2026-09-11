# Silver substitution and CODH function at primary-abstract scope

The [2011 primary abstract](https://pubmed.ncbi.nlm.nih.gov/21774528/) reports
functional Ag-substituted CO dehydrogenase from *Oligotropha carboxidovorans*,
with an Ag-coupled EPR signal after reduction by CO. This is a source-reported
metal-substitution/function association, carried separately from the native Cu-specific
M0107 mechanism proposals (CE-047).

```sh
python scripts/query_atlas_perturbations.py --control-relation codh_2011:Ag-substitution:source-assessment
```

The shared query returns the source-named preparations, four parameter records,
three distinct assay wrappers and spectral context. The wrappers identify
reported endpoints; their full experimental conditions are unqualified.

| Source preparation | Reported endpoint | Value | Inspected condition scope |
| --- | --- | ---: | --- |
| Ag-substituted | Limiting observed rate of enzyme reduction by CO | 8.1 s^-1 | pH, temperature, readout and normalization unstated |
| Source wild type | Limiting CO-reduction comparator | 51 s^-1 | Underlying experiment and condition matching unassessed |
| Ag-substituted | Steady-state kcat | 8.2 s^-1 | pH 7.2; acceptor and normalization unstated |
| Ag-substituted | Steady-state KM | 2.95 µM | pH 7.2; varied analyte not explicitly restated |

The KM is in the article's CO context, but its analyte is not silently filled
in as a qualified CO binding constant. None of the four numbers has an error
or replicate count in the inspected abstract. Missing uncertainty is not zero.
These are four source parameter records, not four independent experiments or
newly admitted Tier-4 observations.

The reported Ag nuclear spin I = 1/2 hyperfine coupling associates an EPR-active
population with the binuclear site after CO reduction. It does not establish
complete Ag occupancy, metal stoichiometry, absence of residual Cu, Ag oxidation
state, coordination geometry or identity with the population producing bulk
turnover. Retained activity remains the authors' attribution to the
Ag-substituted preparation. Metal depletion/reconstitution, apo controls and
Ag/Cu/Mo analyses are unavailable in the inspected scope.

The source WT value of 51 s^-1 is a reduction-rate comparator, not a WT kcat.
The query performs no ratio. Nor does the proximity of 8.1 and 8.2 establish
a rate-limiting step: measurement conditions, normalization, errors and shared
preparation are unknown. The native-enzyme background about aerobic growth does
not become an Ag-enzyme growth, physiological quinone/O2-transfer or direct
CO2-quantitation result.

The [source packet](../data/atlas/study_context/codh_2011/source_qualification.json)
binds the exact EuropePMC primary-abstract response and M0107's DOI citation.
The latter is a bibliography association only; no reference protein accession,
Cu(I) mechanism step or physical specimen is transferred. Both original M0107
proposals and all frozen source records remain unchanged.

The generic `system_assessment` path in the
[shared consumer](ATLAS_PERTURBATION_RELATION.md) resolves source systems,
assays and parameter identities while keeping arithmetic unrequested. It
accepts different endpoints in one reviewed assessment without pretending they
are a matched ratio. Its scalar result and unit remain null and `eligible` is
false, while the positive source assessment and its evidence remain available.
The assessment finding is resolved from the same source packet as the measurement
arms, using `assessment_provider`; it is not copied into a second editable claim.
A nonempty study identity, source-bound evidence and distinct parameter selectors
are required, and declared assay qualification must agree with the source when
that source field is present. These checks preserve provenance, not scientific
validation. Metal replacement is a chemical intervention; it creates no genetic mutant.
The existing quantitative micellar and acetylation relations retain their
stricter ratio rules and outputs. Reuse checks apply the assessment path to
their existing source arms without creating new observations or rewriting
those published relations.

Only the primary abstract was acquired: four requests / 30,214 response-body
bytes in the distinct `codh-2011-silver-substitution` batch. The publisher
request returned 403; the supporting-data lookup returned no entry. This is
not evidence of literature-wide absence. Exact bodies remain in the Git-common
cache and are not redistributed. The
[receipt](../data/atlas/study_context/codh_2011/acquisition_receipts.json)
retains the requests and scope.

The preceding Ibdah1996 inquiry stopped after six new requests / 270,619 bytes.
Its named Trp464 replacement/absolute-activity relation remains unassessed.
The separate inherited `two-substrate-lineages-2024-51831` batch is now at
39 requests / 23,268,387 bytes, recorded in its
[appendix](../data/atlas/study_context/ahas_2005/ibdah_acquisition_appendix.json).
Neither batch resets an older allowance.

The usable gain is a metal-intervention/spectroscopy/endpoint relation that
prevents reduction and turnover constants from collapsing into one activity
label. A competent reader can recover the underlying abstract facts. Manual
source interpretation remains, with no measured curation-time saving, broad
coverage or demonstrated design benefit. Missing full-text controls do not
justify a more detailed metal model or another access-only run. This inquiry
stops here; a new complete primary witness could change its narrower limits.
