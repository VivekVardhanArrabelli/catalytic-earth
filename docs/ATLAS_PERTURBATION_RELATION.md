# Source-bound perturbation relation

One offline consumer now recovers the accepted RA95 2013/2017 and RA61
perturbation comparisons, their exclusions, KE59's unassessed matched-control
question, the human-transketolase endpoint contrast, POX analogue nonbinding beside pyruvate responses, and the beta-barrel benzoate-control conflict. It answers which source-defined perturbations retain a measured
endpoint in a particular background, substrate and assay. It does not assign
generic activity, residue causality, preserved catalytic apparatus or design
success. Current scientific scope remains [CE-024–CE-033](../CLAIMS.md).

## Use the relation

From the repository root, with Python 3.10 or newer and no added dependencies:

```sh
python scripts/query_atlas_perturbations.py --output /tmp/perturbations.json
python scripts/query_atlas_perturbations.py --study ra61_2010
python scripts/query_atlas_perturbations.py --comparison 'tkt_2019:E366Q:kcat'
python scripts/query_atlas_perturbations.py --comparison 'pox_2019:E59Q:kcat'
python scripts/query_atlas_perturbations.py --comparison 'beta_barrel_2022:benzoate-control-to-8AH9'
python scripts/query_atlas_perturbations.py --comparison 'ra95_2017:Y51F-Y180F:kcat'
python scripts/query_atlas_perturbations.py --comparison 'ke59_2012:E230-matched-perturbation'
python scripts/query_atlas_perturbations.py --verify-witnesses --output /tmp/perturbations-with-local-source-check.json
```

This is a repository dataset query. The frozen Atlas-3/10 release and its
installed command are unchanged. JSON output includes observations, comparison
eligibility and reasons, exact construct/sequence providers, assays, substrate
states, source contexts and witness references. A comparison filter retains its
control observations; an unassessed question retains the identified contextual
observations without inventing a measured mutant. Context dictionaries remain
available when rows are filtered so the exclusions travel with the answer.

The Python entry point is `catalytic_earth.atlas_perturbations.project(repo_root)`;
`compare(rows_by_id, request)` exposes the same eligibility rules for explicit
comparison requests over the returned reviewed rows. This helper calculates
candidate arithmetic; it does not independently authenticate a supplied request.
Neither function discovers matched controls by similarity.

## What the same consumer recovers

| Source-defined comparison | Returned result | Limit that remains attached |
| --- | --- | --- |
| 2013 RA95.5-5 K210M / same-table parent | kcat 0.023 / 0.048 = 0.4792; printed efficiency 490 / 490 = 1 | Parameter-specific central values; no statistical equivalence; printed KM units remain conflicted |
| 2013 RA95.5-5 K83M / same-table parent | Positive printed efficiency 2.3 / 490 = 0.004694 | Small positive fitted value is different from nondetection |
| 2013 RA95.0 K210M | Scoped nondetection with null numeric value; ratio ineligible | No numeric detection limit; the unmarked source rows have unresolved technique and conditions |
| 2017 RA95.5-8F Y51F/Y180F paired square | Double / multiplicative reference: kcat 0.021; KM 0.422857; printed efficiency 0.050298 | Missing Asn double cells, thermal confounding and parent-only structural context remain; no microscopic interaction energy |
| 2013 RA95.0 and RA95.5-8 R/S comparisons | Cleavage preference changes from S to R at the accepted scope | Printed selectivity factors remain separate from quotients of rounded efficiency columns; no synthesis-selectivity transfer |
| 2013 RA95.5 R/S comparison | Integrated preference withheld; reported R preference and factor 3.2 retained | Inconsistent S kinetic triplet is not repaired |
| 2010 RA61 Y78F/S87A / named RA61 parent | 2.6 / 0.49 = 5.3061; source factor 5.3 separately retained | Initial-rate endpoint through aldehyde formation, not later cycle steps; exact sequences are unavailable |
| 2012 KE59 E230 replacement question | Unassessed matched comparison, with no mutant/control/value fabricated | Acquired main article has no matched E230 assay; unacquired SI remains unassessed; pKa is not residue assignment |

The original perturbation input scope covers 41 previously curated source table-row contexts,
projected into 106 parameter records: 93 numeric, ten unit-conflicted and
three parameter-unavailable records attached to one nondetection context.
There are 55 declared comparison requests, of which 41 permit the defined
descriptive arithmetic and 14 abstain. One abstention is the separate KE59
assessment, not an experimental observation. These are view/coverage counts,
not new experiments, biological cases, independent replicates or a success rate.
No project experiment or independent expert validation was performed.

## Forward product evidence

The [forward methodol synthesis extension](ATLAS_FORWARD_SYNTHESIS.md) adds
seven parameter records from one primary synthetic-product context and two
precursor comparator contexts: source-reported conversion, isolated yield and
enantiomer ratio components. The complete view therefore has 113 parameter
records; the 55 existing comparison requests and their 41 eligible / 14 abstained
outcomes are unchanged. These are dataset-view counts, not experiments or
independent biological cases.

The source reports 67% conversion, 60.1% isolated yield and R-major composition,
while retaining two unresolved source conflicts: 50 mL × 2 mM versus printed
130 micromol, and reversed R/S retention assignments in Methods versus S12.
The author's R assignment also cites optical-rotation comparison. A strict
greater-than-98.4% ee statement remains structured source context and is not
coerced into an exact central value. The precursor's 0.7% conversion under the
same conditions stays separate from its 44% ee under longer time and more enzyme.

Optional `reaction_id` / `reaction_context` fields carry source-bound,
role-tagged reactants and product. A shared check matches the input participant IDs to the source reaction
reactants, binds the observation substrate ID and matches source-assay
identity/direction. Exact reviewed source bytes bind chemical names and roles.
Product identity is not substituted for cleavage substrate identity; missing
legacy reaction context stays null. Participants and scope come from reviewed
data, not an enzyme-specific runtime branch or an inferred atom map.

## Diels–Alder source effects with an unresolved matched assay

The [Siegel2010 extension](ATLAS_DIELS_ALDER_CONTROLS.md) reuses the same
consumer without runtime changes. It adds three parent DA_20_10 fitted
parameters and two reported mutant activity-reduction factors. Diene and
dienophile KM values have separate parameter IDs and source participant
markers. The factors retain an unqualified assay and cannot become mutant
kinetics, yield or stereoselectivity effects. A new unassessed request preserves
the reported effects while refusing reconstructed parameter-matched controls.

Use `--study diels_alder_2010` or
`--comparison diels_alder_2010:qualified-mutant-parameter`. Strict >80%
conversion and >97% source-assigned stereoisomer-share bounds remain separate
structured source contexts with null central values. The view after that extension
had 118 parameter records and 56 comparison requests: 41 eligible, 15 abstained.
The prior 113 records and 55 comparisons are unchanged. Three new host-local
witnesses bind the article and Figures 1/4; acquisition consumed 14 requests /
502,726 bytes in a distinct cumulative batch. No source bodies are redistributed.

## Cofactor-dependent endpoints remain distinct

The same consumer now projects the [retained human-transketolase evidence](ATLAS_STUDY_CONTEXT.md#variant-kinetics-retain-their-assay-and-parameter-identity).
For `--comparison tkt_2019:E366Q:kcat`, it returns the two turnover operands
plus four context records: WT/E366Q stopped-flow and WT/E366Q NMR. Only the
turnover operands enter the ratio. A researcher can retrieve the counterevidence
without reconstructing the table and assembly packet layouts.

| E366Q result | Common representation | Permitted comparison |
| --- | --- | --- |
| X5P/R5P kcat 0.012 ± 0.001 s⁻¹ versus WT 2.79 ± 0.06 at 20 °C | Numeric, mean and SD; NADH-coupled 340-nm assay | E366Q/WT = 0.004301, about 0.43% of the source central turnover value; no propagated uncertainty or significance claim |
| F6P stopped-flow kforward at 4 °C | Unavailable, null value, source `n.a.` and missing 325-nm reporter reason | Rate ratio abstains; an unavailable reporter is not an observed zero rate |
| F6P acid-quench NMR | Nondetection of covalent-intermediate accumulation, null fraction and detection floor; WT qualitative accumulation retained | Numeric fraction ratio abstains; this endpoint does not measure a formation or turnover rate |

All seven variants contribute kcat and kforward entries, and all five inherited
NMR arms are included. The 19 added view records comprise eleven numeric,
three unavailable, three qualitative-positive and two nondetection results.
Six turnover and three forward-rate ratios are eligible; three reporter-rate
and four NMR-ratio requests abstain. The view after that extension had 137 records and
72 requests, with 50 eligible and 22 abstaining. These are projections of
previously curated published endpoints, not new experiments or independent
replicates. All 118 preceding records and 56 comparison results are unchanged.

A shared `unavailable` kind carries source token, scope and reason separately
from nondetection and an unassessed control. A `qualitative_result` payload
exposes the normalized accumulation statement, explicitly labeled as a project
paraphrase rather than a verbatim quote, without requiring a source-specific
field lookup. Both use null numeric values. Original source parameter/row
objects remain attached; excluded kmax bounds and ambiguous T382E efficiency
text are preserved there without being selected as common numeric records.

The source-defined WT and six variants have explicit missing exact assay
sequences in a small [identity adapter](../data/atlas/study_context/6ha3/perturbation_context.json).
It adds construct/background and NMR-assay identities while numeric values and
NMR results still resolve directly from the unchanged accepted source packet.
Its NMR conditions remain typical method conditions, not authenticated settings
for every variant trace. Table uncertainty is mean ± SD from reported
triplicates, with no assumed independent preparation count. For T382Q, the
reporter explanation is an integration of row-level footnote e in the pKa cell
with the common optical method; it is not a marker printed on each blue cell.

The X5P/R5P donor/acceptor assay is distinct from the F6P donor half-reaction.
Neither the shared unit s⁻¹ nor a source-named protein establishes a valid
cross-assay rate ratio. 6HA3 is the E160Q structure: its partner-copy Glu366
context does not supply E366Q coordinates, a selective partner-only mutation,
causal geometry, productive F6P full-cycle turnover or a design template.

Four existing TKT primary witnesses were copied, after hash checks, from the
temporary cache into the Git-common-directory source cache. No acquisition
occurred. The TKT batch retains its historical lower bound of 7 requests /
3,004,884 response-body bytes; complete cumulative usage and headroom remain
unknown. No source bodies are redistributed.

## Analogue nonbinding does not erase authentic-substrate responses

The [retained POX comparison](ATLAS_STUDY_CONTEXT.md#pox-analogue-binding-does-not-supply-a-generic-activity-label)
now uses the same consumer and eligibility rules, with no runtime or CLI change.
`--comparison pox_2019:E59Q:kcat` returns two DCPIP-turnover operands plus
paired WT/E59Q context for MAP k_on, k_off, K_D_app, pyruvate/DCPIP KM,
and pyruvate/FAD k_app_max and K0.5. These twelve context records never enter the turnover ratio.

| E59Q source result at 25 °C | Executable result | Restriction |
| --- | --- | --- |
| Pyruvate/DCPIP kcat 0.49 ± 0.01 s⁻¹; WT 31.8 ± 0.4 | E59Q/WT = 0.0154088, about 1.54% of the reported central value | DCPIP is an artificial electron acceptor; this is not oxygen-turnover kinetics |
| MAP k_on, k_off and K_D_app are `n.a.` | All three values stay null with a source-reported MAP-nonbinding reason; all three ratios abstain | No zero rate, infinite affinity constant or numeric detection threshold is inferred |
| Anaerobic pyruvate/FAD k_app_max 1.07 ± 0.08 s⁻¹; WT 136 ± 1 | E59Q/WT = 0.00786765, about 0.787% of the reported central value | Apparent saturated processing spans multiple microscopic steps; it is not kcat or an elementary-step rate |

Seven columns across all six variants contribute 42 common parameter records:
39 numeric and three unavailable. Of 35 within-assay mutant/WT requests, 32
permit descriptive arithmetic and three abstain. The view after that extension had 179
records and 107 requests (82 eligible, 25 abstaining); all previous 137 records
and 72 comparison results remain unchanged. These are projections of retained
published evidence, not experiment, enzyme-admission or independent-replicate
counts. The three unselected columns remain in each full source row:
both source-reported efficiencies and the Hill coefficient.
Their values are available context, not unmeasured or missing controls.

Pyruvate KM (E59Q 979 ± 67 mM; WT 1.59 ± 0.01 mM) and single-turnover
K0.5 (888 ± 132 mM; WT 3.4 ± 0.1 mM) are also common records. The consumer
rejects substituting either for MAP K_D_app, or substituting K0.5 for KM,
because their assay, parameter and fitted-model scopes differ. This makes the
constant-transfer restriction executable rather than leaving it only in source
context. These apparent/model-dependent constants are not collapsed into a
generic substrate-affinity label.

MAP forms a reversible covalent conjugate with ThDP and is not further processed.
Its apparent K_D retains the source-model relation k_off/k_on and its reported
micromolar unit; it is not an isolated noncovalent docking constant or pyruvate
affinity. No source-rounded quotient is recomputed or counted as a separate
measurement. The six [source-named constructs](../data/atlas/study_context/pox2019/perturbation_context.json)
have null exact sequences and digests. POX and TKT share a publication DOI,
but have separate enzyme, construct/background and assay identifiers. The same
DOI, kcat parameter name or s⁻¹ unit does not qualify their rate comparison.

The shared unavailable-result filter exposes the different reasons without a
new source-format parser:

```python
from pathlib import Path
from catalytic_earth.atlas_perturbations import project

view = project(Path.cwd())
for row in view["observations"]:
    if row["result_kind"] == "unavailable":
        print(row["id"], row["unavailability"]["reason"])
```

This returns the TKT reporter-absence reasons and POX analogue-nonbinding
reasons through the same fields. It does not infer a shared chemical cause or
pool numerical activity. The exact old cross-context source pointer is also
retained with the E59Q requests. Runtime comparison contexts remain within
one enzyme-study scope; cross-context source prose supplies no arithmetic join.

The Table 2b E59Q footnote-k marker is printed on k_on and applies to the
unavailable MAP group; no separate marker is invented for every cell. The
source's MAP optical path `10 mM` and unstated single-turnover pH remain
unresolved. Table triplicates mean displayed mean ± SD, with no authenticated
independent preparation count. The Figure 8 repeat statement does not turn
those into six replicates. Parameter uncertainty remains distinct from the
unestimated uncertainty of the descriptive ratios.

All four POX source witnesses were already retained for TKT and are reused by
hash without another copy or acquisition: zero requests and bytes. The named
batch retains its lower bound of 7 requests / 3,004,884 bytes with unknown
complete usage and headroom. Source bodies remain host-local. This extension
removes a source-layout join for retrieval and blocks a concrete bad transfer;
no measured curation-time saving, incumbent superiority, causal role or design
success is established.

## A qualitative control conflict stays attached to its construct

The [retained beta-barrel evidence](ATLAS_BETA_BARREL_CONTROLS.md) now uses
the same consumer without runtime or CLI changes. The query
`--comparison beta_barrel_2022:benzoate-control-to-8AH9` returns the six selected
kinetic parameter records, all eight S4 condition arms, the conflicting source
statements and the separate deposited identity. Its explicit target is a
matched ligand-control measurement for RAβb-16.1 / 8AH9. That target remains
unassessed; the published RAβb-16.2 S4 experiment has been assessed qualitatively.

Three source-table ratios for the paired K49E/S51H 16.2 construct relative to
16.1 remain eligible at their own endpoint:

| Parameter | 16.2 / 16.1 central values | Descriptive ratio |
| --- | --- | ---: |
| kcat, min^-1 | 1.6 / 1.5 | 1.0667 |
| KM, uM | 50 / 230 | 0.21739 |
| Printed kcat/KM, M^-1 min^-1 | 30,000 / 6,500 | 4.61538 |

Use `--comparison beta_barrel_2022:16.2-over-16.1:kcat` for one such ratio
with all fourteen records retained as operands or context. This is a combined
substitution contrast, with no isolated K49E or S51H effect. Reported errors
(0.1 for both kcat values; 10 and 40 uM for KM) keep their unknown statistic.
No error is invented for printed efficiencies. Figure 6 says pH 7 and Methods
4.7 says pH 7.5: the shared within-table contrast remains usable, while the
integrated pH stays null and cannot qualify an exact-condition transfer.
Printed S/R factors 36 and 500 remain source context; no R kinetic value,
selectivity ratio or forward-synthesis outcome is reconstructed.

All S4 records are **qualitative**, with null activity and error values. Their
common qualitative payload carries the benzoate dose, preincubation time,
source panel label and axis label. All eight plotted bars are visibly positive.
Only the four 2.5/25 mM arms carry the reviewed observation that they are below
their own panel's zero-addition bar. The zero and 0.25 mM arms carry no
relative-effect ordering. These annotations do not digitize the plot or infer
a normalization, numeric dose ratio, inhibition mechanism, Ki or significance.
The caption's two purified batches are not a per-arm replicate count.

The transfer request preserves both limitations: main-text noninhibition prose
conflicts with the S4 plot, and the caption names 16.2 while 8AH9 names 16.1.
Zero **added** benzoate does not establish ligand-depleted protein. Neither
retained activity nor mutation-informed docking qualifies ligand-independent
catalysis or productive geometry. RAβb-8 K77M and the unspecified Lys53/Tyr17
author assertions remain context; no K53M/Y17F control is invented.

Both exact assay sequences remain null in a small
[sequence-identity adapter](../data/atlas/study_context/beta_barrel_2022/perturbation_context.json).
The original construct providers retain the seven earlier 16-to-16.1 changes,
including the V49K step before K49E. The exact 120-residue deposited sequence
and its digest remain in source context, without being copied into either
assay sequence. Study-scoped methodol identifiers prevent the existing RA95
preparation metadata from being borrowed. Their descriptive name/configuration
relation is not an operational assay or rate equivalence.

This adds fourteen view records (six numeric, eight qualitative) and four
requests (three eligible, one abstaining). The complete view has 193 records
and 111 requests: 85 eligible and 26 abstaining. All preceding 179 observation
objects and 107 comparison objects remain unchanged. These are dataset-view
counts, not experiments, independent replicates, protein admissions or success
rates. The array-index field mappings retain exact parameter markers so a
swapped KM/kcat/efficiency provider fails rather than inheriting meaning from
an index or unit alone.

Three hash-verified witnesses (article PDF/XML and the exact S4 TIFF) were
copied to the durable local source cache: 4,187,601 bytes and zero acquisition
requests. The S4 witness names its ZIP container URL, hash and exact member;
that URL is not represented as a direct TIFF download. All seventeen local witnesses verify at 20,956,262 bytes. The named
Kipnis batch remains cumulative at five requests / 8,449,621 response-body bytes.
The public mmCIF stays in its original tracked path; publisher bodies are not
redistributed by this increment.

This completes the distinct construct/control-conflict question with the
existing qualitative and unassessed concepts. A generic numeric chemical-dose
comparison is not implemented: there are no transcribed numeric S4 operands,
and the existing ratio operation is a genetic-background comparison. Tests
explicitly refuse attempted dose ratios. Another migration of a cached table
would not by itself justify a new run; the next work should resolve a different
scientific bottleneck or demonstrate a useful relation across the assembled
sources.

## Shared representation and eligibility

The [declarative projection](../data/atlas/perturbations/projection.json) is the
only place that maps the different source packet layouts. It supplies source
hashes, JSON pointers, construct/background identities, chemical states,
parameter mappings, result-kind mappings and explicitly named controls. The
consumer contains no enzyme-ID or study-ID branches. Existing source packets
remain byte-identical; values and uncertainty are read from their providers.
The [computational source review](../data/atlas/perturbations/review.json) binds
the exact projection and both public consumer files. The default Python/CLI
query rejects changed bytes before projecting. This protects curated substrate,
direction, endpoint, qualification and missingness mappings as well as source
values; a changed interpretation requires renewed review. Internal candidate
projection for development is explicitly unreviewed and confers no reviewed
source eligibility. These hashes bind the review; they do not prove its chemistry.

Every parameter record retains its entire original parameter and row beside
the common value/unit/uncertainty fields. Construct providers retain whether
a sequence was directly printed or derived, as well as lineage and numbering
cautions. Sequence hashes are checked separately from perturbation/background
provider equality. A sequence-bound construct still does not identify the
physical assay aliquot. Missing RA61/KE59/TKT/POX/beta-barrel assay sequences are explicit and cannot
be borrowed from a nearby name or structure.
The two positive unmarked RA95.0 rows retain their displayed error magnitudes
with unresolved statistic types. Conflicted KM error magnitudes keep their
printed unit without implying a normalized KM. Nondetection has common fields
for its source token, scope, numeric detection limit and nonzero-coercion rule.

Numeric mutation ratios require the same study, assay, substrate, reaction
direction, endpoint, parameter, unit and declared background, and the specified
denominator must be the unperturbed background. Unknown assays, conflicting
units, nondetection and source objections block the comparison. Apparent pKa,
initial-rate observed efficiency and steady-state parameters remain distinct.
No unit conversion, rate pooling, raw-trace fitting or triplet reconciliation
is performed. Source-reported efficiency is not recomputed from kcat and KM.

The four-cell operation additionally requires the parent, two distinct single
substitutions and their exact double in one background. It computes
`qAB / (qA * qB / q0)` for the declared parameter. It cannot substitute the
triple for a missing double. The substrate-preference operation changes only
the source-bound substrate state within one construct/assay and retains the
reported factor separately. Source inconsistencies block its integrated label.

KE59's unassessed request has empty comparison roles and null construct,
sequence, matched-control, assay and measured-value fields. Its five pH-profile
backgrounds and ten parameter values remain addressable as indirect context.
Original KE59, the R1 structural proxy and the R2 pH proxy remain distinct.
RA61's solution-amine and Brønsted-model estimates remain contextual source
evidence and never become protein-mutation observations in this relation.
The beta-barrel packet is included with its construct/control mismatch
explicitly unresolved. Its eight assessed qualitative arms do not become a
matched 16.1/8AH9 measurement.

## Provenance and source retention

Source bindings resolve the five original accepted annotation packets, the
forward-synthesis packet, the Diels–Alder annotation, the retained TKT packets
plus identity adapter, the POX source packet and named-construct adapter, and
the beta-barrel source packet, sequence adapter and acquisition receipt.
Output preserves
study and source-locator context, original source conflicts, missing controls,
thermal/mass evidence and selection limitations. Original primary bodies are
not redistributed. Seven originally acquired, hash-verified files were copied
into `catalytic-earth-source-cache/` under the Git common directory. The
projection records their exact hashes, byte sizes, original URLs and relative
cache locations, including the publisher page that binds the 2017 supplement.
This is durable host-local retention, not a promise of public source availability.
The offline relation needs the committed annotations; primary-source review
also needs the recorded witnesses or separately authorized reacquisition.
The default query checks witness bindings and labels local byte availability
as unchecked. The three Diels–Alder article/figure witnesses brought the set to ten files.
Four retained TKT witnesses brought it to fourteen files (16,768,661 bytes);
POX reuses those same four files without duplicate copies. The beta-barrel
article PDF/XML and S4 TIFF bring the current set to seventeen files
(20,956,262 bytes). `--verify-witnesses` checks all lengths and
hashes, and fails if any file is missing or altered; it never fetches a replacement.

The original relation and methodol extension made no new source requests;
the Diels–Alder extension's distinct budget is reported above. Inherited cumulative usage remains RA95
24 requests / 15,353,338 bytes, RA61 45 / 3,236,259, and KE59 9 / 261,580.
Local copies and repeated projections consume no acquisition allowance.

## Value, review and next bottleneck

The added capability is an executable relation across these packet shapes:
one consumer recovers the comparisons and explicitly refuses wrong assay,
background, substrate, endpoint and source joins. A competent reader could
recover the underlying facts from the incumbent articles. No measured curation
speedup, incumbent superiority or design utility is claimed. This resolves
the current bounded reuse question; it does not establish a universal atlas.

Source and representation reviewers challenged the retained primary witnesses
and projected outputs separately, using GPT-5.6 Sol/ultra. These are correlated
computational checks, not independent human review. The internal
[coordination record](https://github.com/VivekVardhanArrabelli/catalytic-earth/blob/main/work/coordination_perturbation_relation_20260910.md)
records objections and parent adjudications. Adversarial tests cover scientifically
invalid joins, zero-coercion, source conflict, missing controls and provider drift.

The three reconsideration conditions now have a concrete bounded result:
case-specific layout mappings stay in data; existing sequence and source
providers are reused unchanged; and a common consumer returns usable exclusions.
This does not erase the manual effort of defining each panel. Forward methodol
synthesis now supplies a completed product-evidence extension, with a justified
shared reaction/participants primitive and source conflicts retained.

The Diels–Alder test now preserves a partial cross-chemistry relation and a
supported control-assay gap. It demonstrates data-only reuse while failing to
qualify the requested matched product/control inference. Repeating inaccessible
supplement routes or adding another main-text endpoint cannot close that gap.

The TKT extension resolves that cofactor-dependent reuse question. Two small
shared result-detail rules distinguish unavailable parameters and qualitative
observations; all study-specific chemistry, identities and source layout
mappings remain data. The identity adapter still required manual declaration
and source review, so no measured curation saving or incumbent superiority is
claimed. Its useful addition is a queryable refusal to transfer reporter
absence into loss of catalysis, with the positive endpoint beside it.

POX now reuses those missingness semantics without another runtime change.
Adversarial review expanded the initial five-column selection to include KM
and K0.5, so inappropriate MAP/pyruvate constant transfers are also executable
abstentions. Source review narrowed the absence of a structure mapping to the
missing exact assay-specimen mapping; a named deposit is not denied or promoted
into functional geometry. The [POX coordination record](https://github.com/VivekVardhanArrabelli/catalytic-earth/blob/main/work/coordination_pox_perturbation_20260910.md)
records this review. The current handoff and direction review select the next
scientific bottleneck; repeated arithmetic on these settled cases adds no gain.
