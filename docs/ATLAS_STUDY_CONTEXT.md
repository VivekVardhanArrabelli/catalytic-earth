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
