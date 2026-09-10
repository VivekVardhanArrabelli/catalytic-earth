# De novo beta-barrel activity and the benzoate control

The [source annotation](../data/atlas/study_context/beta_barrel_2022/source_qualification.json)
qualifies a consequential conflict in Kipnis et al., *Design and optimization of
enzymatic activity in a de novo beta-barrel scaffold*,
[DOI 10.1002/pro.4405](https://doi.org/10.1002/pro.4405), PMID 36305767,
PMC9601869. The main article, all six supplementary figure groups, and its
explicitly cited structure 8AH9 were acquired and checked.

## A positive functional result with a limited structural interpretation

Two selected variants of this de novo scaffold have published, purified-protein
S-methodol cleavage parameters (main Table 2, page 8):

| Named construct | kcat, min^-1 | KM, uM | Printed kcat/KM, M^-1 min^-1 | Printed S/R efficiency factor |
| --- | ---: | ---: | ---: | ---: |
| RAβb-16.1 | 1.5 ± 0.1 | 230 ± 40 | 6,500 | 36 |
| RAβb-16.2 | 1.6 ± 0.1 | 50 ± 10 | 30,000 | 500 |

The source identifies RAβb-16.2 as the K49E/S51H derivative of RAβb-16.1.
Its parent already contains seven declared changes from RAβb-16, including
V49K. Keep the position-49 lineage V to K to E explicit. These are named
construct relations, not verification of the assayed specimens' full sequences.
Printed efficiencies and selectivity factors remain separate from arithmetic
on rounded parameters; no R parameters are inferred by inversion. The source
does not define the displayed error statistic or per-row sample size.

Methods 4.7 describes absorbance at 350 nm, 25 C, 25 mM HEPES, 100 mM NaCl
and 2.7% acetonitrile. Figure 6 says pH 7, whereas Methods 4.7 says pH 7.5.
The integrated pH is therefore unresolved. The kinetic context is distinct from
crude-lysate screening and the benzoate experiment below.

## The supplementary control does not establish ligand independence

Main Section 2.4, page 9 reports no inhibition by benzoate up to 2.5 mM,
citing Figure S4. The retained S4 image shows bars at 2.5 mM visibly lower than
the same-panel zero-addition bars after both 10 minutes and 14 hours of
preincubation. Activity remains visibly positive. This is a qualitative reading
of the published graph, not a digitized rate, effect estimate, significance test
or inhibition constant.

The S4 caption names **RAβb-16.2**, two independently purified batches, and
250 uM racemic methodol. The crystal discussed in the main text is
**RAβb-16.1**. The noninhibition sentence itself does not name a variant.
The data preserve these two independent limitations: prose/figure disagreement
and the mismatch between the control variant and the structural variant.

Eight condition arms retain the source's four benzoate concentrations
(0, 0.25, 2.5, 25 mM) and two incubation times. No bar values, normalization
definition, per-arm replicate count, error-bar statistic, exact assay buffer,
pH, enzyme concentration or readout are invented. The caption's two protein
batches do not establish a statistical sample size for each bar. A zero-added
benzoate arm is not proof of a benzoate-free protein preparation.

The supported design constraint is to preserve the bound ligand and this
uncertainty when considering the scaffold as a template. The experiment does
not establish ligand-independent catalysis, an uninhibited RAβb-16.1, a
no-effect threshold, or a productive substrate pose. It also does not establish
that benzoate is required or identify a mechanism of inhibition.

## Exact deposited identity is narrower than exact assay identity

The [retained 8AH9 mmCIF](../data/atlas/study_context/beta_barrel_2022/sources/8AH9.cif)
names entity 1 RAbetaB-16.1 and cites the exact paper DOI and PMID; Methods
4.8 explicitly links the structure to that variant. Revision 1.3 is dated
2026-03-04. This is the currently acquired deposit, not an asserted unchanged
paper-time snapshot.

It supplies one exact 120-residue deposited sequence. The first five histidines
are unmodeled; author residue 0 is the following alanine, giving 115 modeled
polymer positions. Preserve the actual string without a guessed initiator or
tag repair. The deposited scheme maps author Lys53 to sequence/label position
59, Tyr17 to 23, and Ser77 to 83. These mappings do not verify a kinetic
specimen's sequence or supply RAβb-16.2's exact sequence.

Three BEZ instances are distinct: label chains B/C/D correspond to atom-site
author chain A residues 201/202/203. C/A202 is adjacent to the selected polar
network. Five atom-pair distances, with exact coordinates and alternate labels,
are retained for reproducibility. Tyr17 OH to this ligand's O2 is 2.820 A;
Ser77 OG alternatives A/B have occupancies 0.5 each and remain separate.
Distances alone do not establish hydrogen bonds, solution protonation,
conformer populations, a catalytic role or geometric tolerances.

The paper reports benzoate of uncertain origin and a clash with its original
modeled carbinolamine pose. Its alternative methodol pose comes from restrained
docking whose poses were selected using mutation evidence. It is not an
independent observation of a productive substrate arrangement. The deposited
disulfide is likewise a structural-specimen feature, not a matched assay control.

## Catalytic assertions retain their actual support

Figure 3f's visible knockout is **RAβb-8 K77M**, whose fluorescence trace is
near-flat compared with its parent. It is not a Lys53 experiment on RAβb-16.1.
No numeric mutant rate, detection limit or mutant folding/active-fraction control
is supplied there, so no numeric zero or isolated microscopic cause is assigned.

The main text separately asserts Lys53 importance and decreased efficiency
after Tyr17 mutation in its RAβb-16.1 discussion. The acquired article and six
SI figure groups do not supply the exact substitutions and quantitative matched
controls behind those statements. They remain qualitative author assertions.
Lysine pKa lowering is a design premise, not a measured titration here.

This adds a primary-study context, two kinetic table rows, eight benzoate
condition arms and one deposited sequence record. It adds no protein-registry
entry, compiled mechanism, new experiment, independent human review, evidence
tier or global design-success/fold-evolvability claim.

## Provenance and acquisition

The [challenge review](../data/atlas/study_context/beta_barrel_2022/source_review.json)
binds the exact annotation, documentation, receipt and deposit. Scientific
content was challenged in three separately prompted computational roles;
agreement is not independent human or experimental validation.

The [Kipnis batch receipt](../data/atlas/study_context/beta_barrel_2022/acquisition_receipts.json)
totals five requests / 8,449,621 response-body bytes. The author-index discovery
was reused from an already metered request in the RA61 investigation and is
not charged twice. Article and SI bodies remain local; the public PDB mmCIF
is retained. The source packet pins the S4 TIFF to its exact XML caption and
archive member, preventing a filename or figure-number guess.

The separate [Jiang2008 acquisition appendix](../data/atlas/study_context/ra61_2010/jiang2008_acquisition_appendix.json)
carries the original RA61 batch forward from 12 to 45 requests, totaling
3,236,259 response-body bytes. Its main article and SI remain inaccessible and
unassessed; metadata and an author summary establish no sequence or lysine
control result. Previous RA61 findings and accepted source packets are unchanged.
The decision to switch sources followed those access failures. No batch was
renamed or reset, and no unchanged failed route is the next research action.
