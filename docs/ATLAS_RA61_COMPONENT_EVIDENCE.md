# Designed catalytic components need different kinds of evidence

In the 2010 RA61 study, substituting both modeled water-contact residues
Tyr78 and Ser87 increases the reported initial-rate second-order endpoint
from **0.49 to 2.6 M⁻¹ s⁻¹** (source ratio **5.3**). The designed motif therefore
has no demonstrated net benefit to that endpoint in the tested parent. This
supports a useful negative for design annotation, without establishing that
water is absent or that proton transfer is unnecessary.
[Lassila, Baker and Herschlag, Table 4](https://doi.org/10.1073/pnas.0913638107).

The [component evidence](../data/atlas/study_context/ra61_2010/component_evidence.json)
separates experimental contrasts from design intent and author inference.
It contains six named RA61 constructs and eleven unique second-order
observation contexts. The RA61/full-substrate value repeated in Tables 1, 4
and 5 is stored once. These are selected published data, not a design cohort,
new experiments, exact sequence records or independently reviewed mechanisms.
The [review](../data/atlas/study_context/ra61_2010/source_review.json) binds the
accepted source annotation under the current computational policy.

| Proposed component | Retained evidence | Supported use and limit |
| --- | --- | --- |
| Tyr78/Ser87 water motif | Same named RA61 background; all five assayed mutant constructs raise displayed (kcat/KM)obs | Record the endpoint response. It does not isolate water occupancy, a microscopic catalytic contribution, compensation or geometry. |
| Interactions with the full naphthyl substrate | Full/minimal substrate rates compared with two solution amines | Retain the author's roughly 500-fold estimate with comparator and assay assumptions. It is not substrate affinity or the effect of a particular pocket residue. |
| Pocket intended to lower Lys176 pKa | Apparent pH-rate/pH-binding profiles and a solution-amine Brønsted model | Retain the author assignment and conditional roughly 10-fold estimate. No direct Lys176 replacement contrast or residue-specific titration is supplied here. |

## What the mutation experiment measures

The full-substrate assay uses naphthaldehyde fluorescence at pH 7.5 and 25 °C,
with 50 mM phosphate, 300 mM NaCl and 5% DMSO. Measurements use soluble,
subsaturating substrate and initial rates before the first turnover. The
reported parameter combines events through aldehyde formation (source
steps 1–3); it supplies neither separate kcat and KM values nor the rate of
one elementary step or later acetone release.

| Table 4 construct | (kcat/KM)obs, M⁻¹ s⁻¹ | Printed mutant/parent ratio |
| --- | ---: | ---: |
| Parent RA61 | 0.49 | 1 |
| Y78F | 1.56 | 3.2 |
| Y78A | 0.98 | 2.0 |
| S87A | 0.79 | 1.6 |
| S87G | 1.8 | 3.7 |
| Y78F/S87A | 2.6 | 5.3 |

Table 4 provides no per-row error or replicate count. The prose's 2–3-fold
summary does not cover every printed single-mutant factor, so the table
values remain explicit. The reported unchanged double-mutant pH profile
has no numerical comparison or stated statistical test; it is not an
equivalence result. Mutant-specific fold, active-fraction and structure
controls are not supplied. Greater solvent access is an untested explanation.

The paper calls the unmutated design “wild type RA61.” It reports inverse-PCR
mutagenesis and His-tag purification, but no complete sequence strings in the
acquired main article or supplement. Figure 2 labels modeled Lys176, Tyr78
and Ser87 in paper-local numbering. Neither those labels nor an earlier
same-name construct establishes an exact sequence or an assay specimen.

## The substrate comparison is a conditional estimate

Table 5 reports full/minimal-substrate ratios of 2,100 for RA61, 5 for
propargylamine and 4 for trifluoroethylamine. The [stored rows](../data/atlas/study_context/ra61_2010/component_evidence.json)
retain each printed factor separately from displayed-value arithmetic.
Ratios of the displayed rates give a further RA61 effect of approximately
414 or 548 relative to the respective amine. These are two comparator-dependent
calculations, not a confidence interval or two new measurements. The author
summarizes the contribution as around 500-fold.

The full substrate uses fluorescence with 5% DMSO. The minimal substrate,
4-hydroxy-4-methyl-2-pentanone, uses acetone proton NMR with 5–8% D2O; DMSO
is unstated in that methods paragraph. Temperature, buffer, pH and NaCl match,
while readout and specified solvent additives differ. The analogue also changes
shape, stereochemistry and products, retains groups capable of binding, and
may change the limiting transition state. It does not isolate hydrophobic
binding energy or the pocket's effect on lysine ionization. Butylamine is
part of the separate Brønsted study, not a Table 5 comparator.

The RA61 apparent pH-rate value is 6.8; its product-binding profile gives
6.9 with an approximate author error of ±0.5. The authors assign these
profiles most simply to catalytic lysine under their mechanism model. Their
roughly 10-fold pKa contribution assumes transfer of solution-amine behavior
(Brønsted slope 0.54 ±0.03, standard error). SI Table S1 gives RA61 effects
182, 32, 10, 6 and 1 for alternative slopes 0.2, 0.4, 0.54, 0.6 and 0.8.
These are model assumptions, not an uncertainty interval or measured
mutational effects. The acquired study's lysine-necessity statement cites the
2008 design paper; it supplies no new matched lysine-replacement assay.

## A product state can distort a progress curve

The [author-linked supplement](https://herschlaglab.stanford.edu/s/177SuppMat.pdf)
reports product-dependent fluorescence loss and models off-pathway iminium
binding of naphthaldehyde. This can reduce both free enzyme and fluorescent
product, producing an apparent burst unrelated to later catalytic steps.
The product-binding fit of 26 µM is an approximate upper limit that assumes
zero fluorescence from bound product; alternative assumptions give 17 or
10 µM. It is neither substrate KM nor catalytic-intermediate affinity.
These limitations motivate the initial-rate regime and remain attached to
its component interpretation.

Figure 2 is a design model. The experimental RA61 crystal lacks ligand, and
the substrate binding orientation is unknown. No measured productive water
position, substrate pose, contact energy or design-distance threshold follows.

## Reuse and boundaries

The annotation links the existing [RA95 perturbation](ATLAS_DESIGNED_ENZYME_OUTCOMES.md)
and [KE59 ionization](ATLAS_KE59_BASE_EVIDENCE.md) records by exact hashes and
JSON pointers. These compare kinds of evidence; they do not rank activities
across different assays or transfer catalytic sites between proteins.
Case facts fit data without another runtime or validator. The article already
reports the component limitations; the atlas adds reusable associations among
design intent, endpoint, observation and inference. No measured advantage
over a competent literature workflow is claimed.

The [acquisition receipt](../data/atlas/study_context/ra61_2010/acquisition_receipts.json)
records the complete named batch at **12 requests / 1,100,587 response-body
bytes**, including errors, discovery and redirects. Both primary PDFs are
retained locally with hashes; source bodies are not redistributed. Existing
source scopes, protected registries, frozen kernels and exposure history are
unchanged. This work adds no new experiment, full mechanism, design-success
rate or evidence-tier promotion.
