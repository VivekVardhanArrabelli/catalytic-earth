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

This file is a source annotation in the repository, not a new installed query
or an expansion of the existing three-observation study-context command.
