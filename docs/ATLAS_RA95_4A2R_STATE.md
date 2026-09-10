# RA95.5-5 attachment and functional context

The source-associated RA95.5-5 assay parent has the same full 258-residue
canonical sequence as
[4A2R](https://www.rcsb.org/structure/4A2R). The deposit explicitly connects
Lys83 to an inhibitor-derived instance. It can therefore accompany the matched
K83M/K210M functional comparisons. This supports a construct and attachment
association, while the complete reacted chemical graph and mutant structures
remain unresolved.

```sh
python scripts/query_atlas_perturbations.py --state-link ra95_2013:RA95.5-5-states --with-comparisons
```

This returns the existing SI Table 2 parent and three engineered derivatives:
12 parameter records and nine comparison requests. Six ratios are eligible;
all three KM ratios abstain because the source's printed unit remains
unresolved. `--with-comparisons` selects existing ratio or multiplicative comparisons whose explicit
`denominator` or `parent` is one of the linked observation IDs, then includes
all their role and context observations. Only the three parent observation IDs
belong to the state link. The option adds retrieval, without assigning a crystal
state to a mutant or turning a ratio into a chemical cause. Without the option,
the state query continues to return its parent observations alone.

| Engineered derivative / matched parent | kcat ratio | Printed kcat/KM ratio | What follows |
| --- | --- | --- | --- |
| K83M | 0.00068 / 0.048 = 0.0142 | 2.3 / 490 = 0.00469 | The approximately 213-fold efficiency reduction is distinct from the approximately 71-fold turnover reduction |
| K210M | 0.023 / 0.048 = 0.479 | 490 / 490 = 1.00 | Unchanged displayed efficiency does not establish an unchanged turnover parameter or a universally irrelevant residue |
| K83M/K210M | 0.000047 / 0.048 = 0.000979 | 0.085 / 490 = 0.000173 | Small positive reported values do not identify another catalytic group |

These are descriptive ratios of rounded source values, with no propagated
uncertainty or significance test. Original numerical errors, KM conflict and
fluorescence limitations remain in the functional provider. The separate main
UV-vis and enantiopure assays cannot replace the SI Table 2 parent denominator.
No folding, active-fraction or mutant-structure control in the retained evidence
isolates a chemical contribution from other substitution effects.

## Construct and chemical-state boundaries

The [2013 article](https://pmc.ncbi.nlm.nih.gov/articles/PMC3720730/)
accession codes assign RA95.5-5 to 4A2R; its title, primary citation and full
canonical sequence agree. Supplementary Figure 5 prints the same tagged string,
SHA256 `2555aec775f6848faca6a5f1a43fb1cd4a72ae077c2bcc7aafb3baf2662d76df`.
Met1 and positions249–258 have no modeled coordinates. The deposit labels
246–258 as expression tag, while the source packet separately records the
terminal251–258 `LEHHHHHH` suffix; neither scope is silently trimmed. Exact
sequence equality does not establish physical assay/crystal aliquot identity.

Methods/S20/P42 reports preparing inhibitor4 by Dess-Martin oxidation of
100 mg methodol (1.2 equivalents, chloroform,1h at room temperature), followed
by silica chromatography. The reported MALDI assignment is `[M+H]+`, with
242.09 both calculated and measured; its unusual label/value is preserved
without correction. The author-reported literature-matching1H NMR remains
separate from independently authenticated spectra or exact material identity.

The source reports inhibitor4 trapping through a Schiff base to a stable
vinylogous amide and exclusive Lys83 modification for this variant. Its
Supplementary Table 3 identifies the ligand as 3NK at Lys83. In the current
CIF, `_struct_conn` and `_pdbx_modification_feature` each retain two alternative
Lys83 NZ–3NK C13 attachments. The ligand is label chainB / authorA1083;
protein Lys83 is label/authorA83. The connection rows report1.343/1.346 Å,
unknown bond order (`?`) and leaving-atom flag `one`. Two alternatives are
not two attachment sites or two simultaneous inhibitor molecules. No Lys210
ligand connection is present in the complete deposited connection inventory;
this does not establish absent Lys210 chemistry during turnover.

The 3NK component definition names the free diketone, C15H14O3. Its dictionary
contains C13=ONA, but both coordinate alternatives omit ONA and retain the
C12 hydrogen names H121/H122. Thus the precursor name, deposited attachment
endpoints and source-proposed reacted chemistry are separate evidence. Joining
unchanged component dictionaries and dropping the absent oxygen would not
establish the complete reacted bond orders, tautomer or protonation. The source
prose's chemical-position label C2 is also distinct from CIF atom name C2,
which lies in the aromatic ring. No source-scheme atom map is asserted.

3NK alternatives A/B carry occupancy0.67/0.33; Lys83 and Lys210 NZ are
nonalternate at1.00. The article describes the ligand poses as70:30; that
source ratio stays separate from current deposited occupancies. Coordinates, model identity and original occupancies stay
intact. No averaged ligand, joint-state probability or solution/kinetic
population is inferred. This packet projects source rows only; it does not
add a distance catalogue or reinterpret the deposited bond distances.

## Conditions, reuse and remaining evidence

The source describes 50–100-fold inhibitor excess, overnight derivatization at
30°C, then size-exclusion purification and crystallization. RA95.5-5 crystals
were grown with microseeding at28°C, pH8.5, with23% PEG3350; diffraction was
collected at100K. Source phosphate is0.1M, whereas deposit details say0.2M:
the normalized concentration remains null. The scalar deposit pH is unknown,
while its detail text explicitly supplies8.5. None of these conditions is
transferred to the29°C/pH7.5 racemic-methodol fluorescence assay.

The existing canonical-sequence state relation and declarative deposit
projector are reused without a chemical-runtime change. The optional comparison
filter works by shared role/observation IDs, including both ratio and paired
comparison requests. Source facts reside in
`data/atlas/study_context/ra95_2013/chemical_state.json`; retained CIF, selections,
projection and review reside in `data/atlas/deposit_context/ra95_4a2r`.
The previous 193 parameter records,111 comparisons, source providers and8F
state relation are unchanged. Manual interpretation and review remain costs;
no measured time saving, incumbent superiority or new catalytic-switch discovery
is claimed. The article already describes that switch.

One public CIF request added707,575 response-body bytes to the existing
`designed-retroaldolase-ra95-giger2013` batch. Cumulative use is27 requests /
17,298,809 bytes under100 /31,457,280; acquisition is stopped. Cached article
and supplement witnesses were reused without requests or redistribution.

The bounded question is answered: exact parent association and deposited
attachment topology are supported. Complete reacted chemistry, physical
preparation identity and causal mutant effects remain open. This does not add
a project experiment, protein admission, mechanism compilation, evidence tier,
productive solution template or demonstrated design capability.
