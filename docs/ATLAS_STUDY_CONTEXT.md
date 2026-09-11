# Atlas study-context packets

Study-context packets connect a deposited arrangement to measured observations
only at the identity and evidence strength directly supported by the retained
sources. They sit beside Atlas source drafts: they do not change frozen Atlas-3,
Atlas-10, or current702 rows, and they do not increase an Atlas evidence tier.

The first packet covers human transketolase E160Q with the F6P-ThDP adduct in
PDB 6HA3. It supplies a reproducible coordinate projection and separates three
experimental endpoints:

- acid-quench NMR intermediate accumulation;
- pre-steady-state reversible F6P-ThDP formation kinetics; and
- steady-state X5P/R5P turnover.

This distinction matters because the turnover substrate context is not the
deposited F6P donor state. The packet joins the first two observations to the
arrangement only as same-study, same-reported-variant associations; it does not
claim identical preparations or conditions, crystal-to-solution state identity,
or geometry-to-rate causation.

Run the deterministic validation with:

```bash
python scripts/validate_atlas_study_context.py
```

The validator reads chemistry selections from the packet, parses the retained
mmCIF with the shared strict parser, recomputes selected atom facts and geometry,
checks component-dictionary bonds separately from deposited connections, and
requires the review pins to remain current.

## F6P adduct reversal and donor cleavage are different transitions

The retained Supplementary Methods distinguish two exits from F6P–ThDP.
Equation 8 assigns `k_reverse` to return toward the noncovalent F6P complex.
Equation 3 separately describes donor cleavage to DHEThDP plus E4P, labelled
by equilibrium constant K3. K3 is not a kinetic rate, and the stopped-flow
fit supplies no parameter for that cleavage edge.

| Source-model transition | E160Q evidence carried by the relation |
| --- | --- |
| Noncovalent F6P complex → F6P–ThDP | Fitted `k_forward` 5.91 ± 0.43 s⁻¹ at 4 °C |
| F6P–ThDP → noncovalent F6P complex | Fitted `k_reverse` 0.47 ± 0.23 s⁻¹ at 4 °C |
| F6P–ThDP → DHEThDP + E4P | Source scheme and scissile-bond assignment; no assigned cleavage rate |
| F6P–ThDP accumulation | Qualitative acid-quench NMR after 30 s at 20 °C; no cleavage fraction |

Extended Data Figure 1c names the formed ThDP C2–F6P C2x bond and the
distinct scissile C2x–C3x bond. The project associates these labels with
deposited T6F C2–CF2 and CF2–CF3. Both are single bonds in the retained
dictionary and remain present in the 6HA3 conjugate. Existing distances
1.544496 and 1.604779 Å are model geometry, not rates. This nomenclature
correspondence is a project interpretation, not an observed free-substrate map.

```sh
python scripts/query_atlas_perturbations.py --model-link tkt_2019:E160Q:F6P_transitions
```

The shared query returns the
[source-model relation](../data/atlas/study_context/6ha3/f6p_transition_context.json),
its exact existing formation/NMR observations, contextual reverse parameter,
assays and arrangement. It checks transition direction, parameter bindings,
state-observation identity and deposit bond locators. Attaching the reverse
parameter to the cleavage transition fails; an unassigned parameter remains
null with an explicit reason, never zero. No measurement or arithmetic
comparison is added. Source review supplies scientific meaning; these checks
cannot independently detect a coherently falsified source interpretation.

The supported result is a partial source-described bond/transition relation.
An atom-resolved elementary step remains unestablished: the retained scheme
does not supply the before-state graph, protonation/tautomer states or
electron/proton sequence. The 325-nm reporter observes AP-band depletion,
with NMR supporting the conjugate assignment; it does not isolate C–C
bond-making. Accumulation does not establish zero cleavage, and acid-isolated
DHEThDP would be a conjugate acid. No K2 calculation combines the separate
assays. Same reported E160Q identity does not establish identical preparations,
crystal/solution conformers, geometry–rate causation or productive F6P turnover.
The M0219 direction and exact-sequence state-link contract remain separate.
[Methods and equation 3/8 schemes](https://media.springernature.com/original/springer-static/esm/art%3A10.1038%2Fs41586-019-1581-9/MediaObjects/41586_2019_1581_MOESM1_ESM.pdf),
[Extended Data legends](https://www.nature.com/articles/s41586-019-1581-9),
[Table 2a and footnote c](https://www.nature.com/articles/s41586-019-1581-9/tables/2).

This closes the bounded question at a useful partial relation. Original source
packets and observations stay unchanged. The link resolves multiple source-bound
endpoints without requiring an exact assay sequence; reuse across a second case
still needs demonstration. No source requests, measured curation-time saving
or incumbent advantage is claimed.

## Partner-subunit context

An additive [assembly packet](../data/atlas/assembly_context/6ha3/spec.json)
resolves the selected partner-subunit Glu366 atoms in 6HA3 assembly 1. Operator
2 maps `(x, y, z)` to `(-x, y, -z)`; Glu366 OE1 in that copy is 2.804089 Å
from Gln160 NE2 in operator 1. The deposited author chain is A for both copies;
their operator identities distinguish them. Label asym B is the T6F component,
not a second protein chain. A single-copy crop therefore omits a group that the
study assigns a cofactor-activation role. This is an omission warning, not a
minimal-site prescription or a distance target.

The functional evidence is deliberately separated:

| Source observation | Permitted reading |
| --- | --- |
| Fig. 1d: E366Q and E165Q show no measurable covalent-intermediate accumulation after F6P acid quench; WT, E160Q and E160A accumulate F6P–ThDP | Qualitative endpoint with an unknown numeric detection floor; not a zero formation rate |
| Table 2a: E366Q X5P/R5P turnover has kcat 0.012 ± 0.001 s⁻¹, versus WT 2.79 ± 0.06 s⁻¹ | Residual turnover on a separate substrate pair; not productive F6P turnover |
| Table 2a, footnote e: the E366Q pre-steady-state reporter is unavailable | Absence of the required 325-nm signal is not a measured zero kinetic rate |

These are project-authored projections of the retained
[primary study](https://www.nature.com/articles/s41586-019-1581-9) and
[Extended Data Table 2](https://www.nature.com/articles/s41586-019-1581-9/tables/2).
The E366Q experiment is not the E160Q crystal preparation or a selective
partner-only mutation. The deposited assembly is author/PISA-defined and
explicitly records `experimental_support=none`. Assembly expansion does not
establish solution oligomerization, protonation, low-barrier hydrogen bonding,
or geometry-to-function causation. Only selected atoms are represented.

```bash
python scripts/build_atlas_assembly_context.py --query
python scripts/build_atlas_assembly_context.py --check
```

The shared operator engine preserves model, author and label residue identity,
insertion code, alternate locations and occupancy. Operator products follow
the [wwPDB expression convention](https://mmcif.wwpdb.org/dictionaries/mmcif_pdbx_v50.dic/Items/_pdbx_struct_assembly_gen.oper_expression.html).
Distances are geometric candidates; alternate labels do not establish a joint
conformer population or a chemical bond. Chemistry and source interpretations
live in data and are pinned by computational source review. The existing study
packet, frozen kernels and evidence tiers remain unchanged.

## Variant kinetics retain their assay and parameter identity

The additive [functional comparison](../data/atlas/study_context/6ha3/functional_comparison.json)
curates all seven human-transketolase rows of the retained Extended Data Table
2a. It links the five already reviewed F6P acid-quench NMR arms without counting
them again. The source's pKa titration column and separate pyruvate-oxidase
table are outside this comparison. These are published-data summaries from one
study, not new experiments, independent validation or additional atlas cases.

| Reported variant | X5P/R5P kcat, s⁻¹, at 20 °C | F6P-adduct kforward, s⁻¹, at 4 °C | F6P acid-quench NMR context |
| --- | --- | --- | --- |
| Wild type | 2.79 ± 0.06 | 9.06 ± 0.72 | F6P–ThDP accumulated |
| E366Q | 0.012 ± 0.001 | Reporter unavailable | No measurable accumulation |
| E160Q | 0.54 ± 0.01 | 5.91 ± 0.43 | F6P–ThDP accumulated |
| E160A | 0.21 ± 0.02 | 8.33 ± 1.21 | F6P–ThDP accumulated |
| E165Q | 0.109 ± 0.002 | Reporter unavailable | No measurable accumulation |
| T382E | 4.30 ± 0.07 | 11.04 ± 0.62 | Not in the retained panel |
| T382Q | 0.25 ± 0.01 | Reporter unavailable | Not in the retained panel |

The table reports triplicate measurements and mean ± SD; it does not supply
raw replicates or establish independent biological-preparation counts. The NMR
panel has no retained numeric detection floor or intermediate fraction. Neither
reporter unavailability nor an absent panel arm is a zero rate.
For T382Q, the reporter explanation integrates row-level footnote e (printed
in its pKa cell) with the common stopped-flow method; its blue kinetic cells
themselves say only `n.a.`.

E160A's reported central values give 0.919 times the wild-type F6P kforward
and 0.0753 times its X5P/R5P kcat. These are two separate within-assay ratios
of source-model fitted parameters, with no propagated uncertainty or test of
equivalence of raw transients. Their substrates, temperatures and endpoints
differ. An adduct-bearing arrangement or F6P
formation rate cannot be substituted for the X5P/R5P activity label, and these
data do not establish productive F6P turnover or a causal geometric effect
(CE-024). [Primary table and footnotes](https://www.nature.com/articles/s41586-019-1581-9/tables/2).

The machine-readable data also preserve qualifications that a flat extraction
of the table headers would lose:

- T382E and T382Q use steady-state **K0.5 and kcat/K0.5**, not KM and
  kcat/KM (footnotes f/g). Their steady-state Hill coefficients, 1.40 ± 0.06
  and 0.80 ± 0.04, remain separate from the F6P stopped-flow Hill coefficient.
- Wild-type and T382E noncovalent ES-formation kmax values are **>600 s⁻¹**
  because of instrument dead time. They remain lower bounds, not values of 600.
- The T382E efficiency cell visibly reads `34.127`. Its punctuation remains
  unresolved. The separate calculation `4.30 / (126 × 10⁻⁶) = 34126.984`
  M⁻¹ s⁻¹ is an arithmetic witness, not a silent correction of that source cell.
- E160A's reverse-rate SD, 0.99 s⁻¹, exceeds its central value, 0.62 s⁻¹.
  Both are retained; no equilibrium ratio or uncertainty is inferred from them.

The stopped-flow fit distinguishes the source-described monophasic wild-type
trace from biphasic variant traces. Its kforward/kreverse is not equated with
the NMR microscopic K2, and the different assays' KM and K0.5 parameters are
not pooled as interchangeable affinity constants. Exact source-observation IDs
and metric mappings identify numerical values reused from the earlier packets.

All facts live in data; this extension adds no runtime branch or validator.
The original study and assembly packets remain byte-identical. The
[source review](../data/atlas/study_context/6ha3/functional_review.json) pins the
comparison and retained input records. Source-body hashes and public locators
are provided, but publisher bodies are not redistributed; exact transcription
review therefore depends on access to those bodies. No curation-time saving or
advantage over a competent reading of the paper is claimed.

For a repository-local view of the two numerical endpoints:

```bash
python - <<'PY'
import json
from pathlib import Path
data = json.loads(Path('data/atlas/study_context/6ha3/functional_comparison.json').read_text())
for row in data['variants']:
    rate = row['stopped_flow']['k_forward']
    print(row['reported_variant'], row['steady_state']['k_cat']['value'],
          rate['value'], rate['status'])
PY
```

The [common perturbation query](ATLAS_PERTURBATION_RELATION.md#cofactor-dependent-endpoints-remain-distinct)
now returns all seven kcat records, all seven kforward records and all five NMR arms, preserving
reporter-unavailable, qualitative and nondetection results. Use
`python scripts/query_atlas_perturbations.py --comparison tkt_2019:E366Q:kcat`
to retain the WT control and the different F6P contexts beside its turnover
ratio. Other table columns remain in the source annotation; the existing
installed three-observation study-context command is unchanged.

## POX analogue binding does not supply a generic activity label

The same study's [POX comparison](../data/atlas/study_context/pox2019/functional_comparison.json)
curates all six Extended Data Table 2b rows for reported *L. plantarum* pyruvate
oxidase. Its three assay contexts remain distinct:

- MAP analogue binding forms a covalent MAP–ThDP conjugate, monitored at
  310 nm. The analogue is not further processed because of its stable C–P bond.
- Anaerobic pyruvate single-turnover processing is monitored through FAD
  reduction at 457 nm. Its apparent saturated rate combines several microscopic
  steps; it is not an isolated decarboxylation rate.
- Pyruvate steady-state activity is measured through reduction of DCPIP at
  600 nm. DCPIP is an artificial electron acceptor replacing oxygen.

| Reported variant | MAP K_D_app, µM | Pyruvate/FAD k_app_max, s⁻¹ | Pyruvate/DCPIP kcat, s⁻¹ |
| --- | --- | --- | --- |
| Wild type | 13.7 | 136 ± 1 | 31.8 ± 0.4 |
| E59Q | Unavailable: source reports no MAP binding | 1.07 ± 0.08 | 0.49 ± 0.01 |
| H89N | 73.1 | 121 ± 5 | 26.0 ± 0.5 |
| H89A | 185.6 | 92 ± 2 | 20.1 ± 0.3 |
| E60Q | 137.5 | 91 ± 3 | 20.2 ± 0.3 |
| E60A | 282.4 | 113 ± 2 | 23.3 ± 0.6 |

All three methods specify 25 °C. The table reports triplicates and mean ± SD;
its derived MAP K_D_app column supplies no SD. Figure 8's statement that
experiments were independently repeated twice does not create extra table
observations or justify treating the table as n = 6.

E59Q's source-reported fitted pyruvate rates remain positive despite the MAP
nonbinding statement (CE-025). Its central values are 0.00787 times wild type
for FAD-reported processing and 0.0154 times wild type for DCPIP turnover.
Each is a separate within-assay ratio, without propagated uncertainty or a
statistical test. No oxygen-turnover rate, general activity threshold or exact
protein-preparation equivalence is established. [Table 2b and footnotes h–k](https://www.nature.com/articles/s41586-019-1581-9/tables/2).

The same qualification matters for apparent affinity. For example, E60A's
central MAP K_D_app is 20.6 times wild type, while its saturated pyruvate/FAD
processing rate is 0.831 times wild type. The quantities describe different
ligands and fitted models. MAP K_D_app = k_off/k_on includes the covalent
conjugate; it is neither an isolated noncovalent docking constant nor the
pyruvate K_M or single-turnover K0.5. The latter retains the source's
pre-equilibrium interpretation within its cooperative model. Reported quotient
values retain their formula and units, including M⁻¹ versus mM⁻¹; they are not
recounted as independent measurements or replaced by recalculated values.
For example, the source prints E60A's single-turnover efficiency as 12.5,
whereas 113/9.0 gives 12.56 mM⁻¹ s⁻¹ from displayed inputs. The annotation
retains 12.5 without reconstructing unreported fit precision.

The comparison also links two distinct reasons for unavailable parameters:
TKT E366Q lacks the stopped-flow reporter, whereas POX E59Q is reported not to
bind the analogue. This exact-pointer reuse prevents a common `n.a.` token
from erasing chemical identity or becoming zero activity. It establishes no
shared residue mechanism, substrate specificity or transferable rate.

Two methods limitations remain explicit in the data. The MAP paragraph prints
an optical path length of `10 mM`, so the normalized length is unresolved.
The single-turnover paragraph does not state pH; pH 6.0 from the other methods
is not silently assigned to it. The retained
[Supplementary Methods](https://media.springernature.com/original/springer-static/esm/art%3A10.1038%2Fs41586-019-1581-9/MediaObjects/41586_2019_1581_MOESM1_ESM.pdf)
printed pages 8–9 define the three assays and equations 9–12.
The differing MAP spellings in those methods and the Figure 8 legend are also
retained; no exact external chemical identifier or atom map is inferred.

This adds a second enzyme-context comparison from one study, using the same
assay descriptors and value/status/SD/unit/parameter concepts. It requires no
runtime or validator change. The [computational review](../data/atlas/study_context/pox2019/functional_review.json)
pins the source annotation; it is not independent human review or validation
of the paper's hydrogen-bond hypothesis. No mechanism, protein registry entry,
experiment or evidence tier is added. A competent reader can recover these
facts from the source; the atlas adds reusable assay identity and prevents
invalid transfers. No curation speed or comparative accuracy is claimed.

This POX annotation is repository-local. Exact source bodies remain retained
locally and are not redistributed. New scientific-source requests/bytes are
zero; the inherited batch remains at a metered lower bound of 7 captures /
3,004,884 bytes with complete accounting and remaining headroom unresolved.
