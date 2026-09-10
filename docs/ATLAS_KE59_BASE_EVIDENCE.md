# KE59 separates a programmed base from evidence of its catalytic role

The acquired Khersonsky 2012 KE59 article does **not establish an exact
construct-matched E230 perturbation comparison**. It provides named variant
substitutions and pH-profile parameters, with a tentative author assignment to
E230. The main text has no isolated E230 replacement assay or complete sequence
strings. Its supplement could not be acquired, so this is a finding about the
retained main article, not an absence claim about the complete study or
literature (CE-027).
[Primary article](https://pmc.ncbi.nlm.nih.gov/articles/PMC3387081/).

## What the source does support

All five Table 2 pKa pairs are retained in the
[source assessment](../data/atlas/study_context/ke59_2012/source_qualification.json).
These are apparent pKa estimates from different kinetic endpoints, measured
with 5-nitrobenzisoxazole across pH 5-8.5. They are not residue-specific
titrations or measurements of a microscopic elementary step.

| Reported variant | pKa from kcat | pKa from kcat/KM |
| --- | ---: | ---: |
| R2-4/3D | 6.1 | 6.3 |
| R4-5/11B | 5.5 | 6.7 |
| R8-2/7A | 6.2 | 6.5 |
| R9-1/4A | 6.5 | 6.5 |
| R13-3/11H | 6.7 | 6.5 |

The adjacent prose describes a 6.1-6.7 range, while the table prints 5.5 for
R4's kcat-derived pKa. Both remain visible; no correction or monotonic trend is
inferred. The main table supplies no uncertainties. Complete buffer-series,
temperature, replication and fitting details remain unresolved here. Routine
fixed-pH kinetic conditions are not transferred to the varied-pH experiment.

The authors tentatively associate the acidic pH shoulder with E230. That
interpretation remains separate from the fitted values and cannot establish
which residue titrates, whether E230 is indispensable, or whether another
catalytic contribution exists.

## Three different starting constructs

The original KE59 design was unstable and could not be purified to homogeneity.
The source warns that soluble misfolded protein could affect its activity
estimate. Two mutation-containing variants serve different proxy roles:

- **R1-7/10H** is the structural proxy, with eight consensus substitutions.
- **R2-4/3D** is the early pH-profile proxy, with eight consensus substitutions
  plus V80A.

The assessment preserves seven named construct contexts: original design,
R1, and the five pH-series variants. Table 1's substitution lists are retained,
but they are not full sequences or verified assay specimens. This paper's
residue numbering is one lower than the earlier publication because the
N-terminal methionine is omitted. No PDB or UniProt position mapping follows.

E230 is absent from the selected declared substitution lists. This alone does
not establish exact sequence retention or unchanged catalytic function. Nor is
the whole designed apparatus unchanged: R13 includes V80A and S179T, and the
source describes altered W109 rotamers and inhibitor binding orientation.

## What a downstream design dataset must keep separate

The record distinguishes declared substitutions, apparent pKa parameters,
author interpretation of structures, inhibitor-pose limitations, and MD-based
mechanistic proposals. The authors warn that benzotriazole inhibitor poses may
not represent catalytic binding. Their MD analysis also reports no correlation
between kcat and relative E230-substrate positioning. No coordinates were
acquired or remeasured by this project.

The [RA95 comparison](ATLAS_DESIGNED_ENZYME_OUTCOMES.md) supports
background-and-parameter-specific substitution sensitivity using acquired
sequence and assay evidence. KE59 currently supports indirect base context.
Neither supports an automatic label that the programmed catalytic role was
retained or relocated across an entire lineage. The assessment leaves all three downstream catalytic labels null and keeps
unlike evidence separate for future dataset use; no runtime consumer or label
enforcement is implemented. The published outcome combines design on an IGPS
scaffold, consensus mutations, mutagenesis and screening. It does not isolate
the design contribution or estimate prospective design success. No
cross-chemistry rate comparison or accuracy gain is claimed.

## Acquisition and review boundary

The [acquisition record](../data/atlas/study_context/ke59_2012/acquisition_receipts.json)
accounts for nine serial requests and 261,580 response-body bytes in the
distinct `designed-kemp-eliminase-ke59-khersonsky2012` batch. It includes an
empty XML 404, download-challenge HTML, a not-open-access API error, publisher
403, a 404, a redirect and two backend errors. Only the primary article HTML is
usable study content. PDF-like filenames do not imply acquired PDFs.

The [review](../data/atlas/study_context/ke59_2012/source_review.json) binds the
accepted assessment and documentation. Source bodies are locally retained and
hash-bound, not redistributed. Repeating the same inaccessible routes is not
the next action. The source-qualified negative is useful without promoting it
to paper-wide absence, an enzyme knockout, a compiled mechanism, a registry
admission, independent human review or a project-run experiment.
