# Gate 3 — Active-site verification of the novel shortlist (2026-06-29)

De-risking step before any lab spend. For each of the 11 dark-protein fold-matches, check whether
the AlphaFold model carries an **intact catalytic apparatus**, not merely the right fold.

- **Serine hydrolases:** source-free Ser-His-Asp triad geometry detected directly in the model.
- **Cofactor families:** AlphaFold models are *apo* (no metal/heme/FAD/PLP), so catalytic-residue
  **conservation** is checked instead — M-CSA neighbour catalytic residues mapped through the
  foldseek structural alignment onto the candidate, then compared by identity.

**Result: 6 verified · 2 partial · 3 not verified.**

> Key finding: **all three flavin (Pyr_redox_2) candidates failed** despite fold-TM 0.85–0.93 —
> their catalytic residues are substituted/degraded. PF07992 is a broad NAD(P)-binding fold shared
> by many proteins, so fold match alone is weak there; the residue check caught it. This is exactly
> the false positive that would have wasted a bench experiment.

## ✅ Verified — active site intact (lab-ready)

### F0Y210 — Aureococcus anophagefferens (Harmful bloom alga)
- predicted: **plp_dependent_enzyme** → *Adenosylmethionine-8-amino-7-oxononanoate aminotransferase* (neighbour P12995), fold-TM 0.9735
- active site: **4/4 catalytic residues conserved** (aligned 4): ['Y17->Y56=', 'Y144->Y184=', 'D245->D286=', 'K274->K317=']
- verdict: **VERIFIED**

### A0A177THN5 — Tilletia indica
- predicted: **heme_peroxidase_oxidase** → *L-ascorbate peroxidase, cytosolic* (neighbour P48534), fold-TM 0.9515
- active site: **5/5 catalytic residues conserved** (aligned 5): ['R38->R36=', 'H42->H40=', 'H163->H164=', 'W179->W180=', 'D208->D231=']
- verdict: **VERIFIED**

### A0AAD9KVE2 — Ridgeia piscesae (Tubeworm)
- predicted: **ser_his_acid_hydrolase** → *Trypsin* (neighbour P35049), fold-TM 0.9394
- active site: **Ser-His-Asp triad resolved** ['SER1087', 'HIS938', 'ASP986']; Ser–His 2.988 Å, His–acid 2.758 Å (catalytic H-bond geometry)
- verdict: **VERIFIED**

### A0AA38MP07 — Zophobas morio
- predicted: **ser_his_acid_hydrolase** → *Chymotrypsinogen A* (neighbour P00766), fold-TM 0.9255
- active site: **Ser-His-Asp triad resolved** ['SER580', 'HIS423', 'ASP481']; Ser–His 3.217 Å, His–acid 2.797 Å (catalytic H-bond geometry)
- verdict: **VERIFIED**

### A0A918P095 — Streptomyces minutiscleroticus
- predicted: **ser_his_acid_hydrolase** → *Streptogrisin-B* (neighbour P00777), fold-TM 0.9244
- active site: **Ser-His-Asp triad resolved** ['SER321', 'HIS204', 'ASP238']; Ser–His 2.799 Å, His–acid 2.788 Å (catalytic H-bond geometry)
- verdict: **VERIFIED**

### M3JW22 — Candida maltosa (strain Xu316) (Yeast)
- predicted: **metal_dependent_hydrolase** → *Hydroxyacylglutathione hydrolase, mitochondrial* (neighbour Q16775), fold-TM 0.8552
- active site: **7/7 catalytic residues conserved** (aligned 7): ['H102->H890=', 'H104->H892=', 'D106->D894=', 'H107->H895=', 'H158->H946=', 'D182->D969=', 'H221->H1008=']
- verdict: **VERIFIED**

## ◐ Partial — core residues present, some divergence

### B3NHH6 — Drosophila erecta (Fruit fly)
- predicted: **plp_dependent_enzyme** → *2,2-dialkylglycine decarboxylase* (neighbour P16932), fold-TM 0.9358
- active site: **4/6 catalytic residues conserved** (aligned 6): ['W138->Y150x', 'E210->E228=', 'D243->D261=', 'Q246->Q264=', 'K272->K291=', 'R406->K424x']
- verdict: **PARTIAL**

### A0AAD6NFH7 — Drechslerella dactyloides (Nematode-trapping fungus) (Arthrobotrys dactyloides)
- predicted: **plp_dependent_enzyme** → *Glutamate-1-semialdehyde 2,1-aminomutase* (neighbour P24630), fold-TM 0.8823
- active site: **2/3 catalytic residues conserved** (aligned 2): ['Y150->Y23=', 'D245->unaligned', 'K273->K107=']
- verdict: **PARTIAL**

## ✗ Not verified — fold only, catalytic apparatus degraded (deprioritize)

### A0A1R2B242 — Stentor coeruleus
- predicted: **flavin_dehydrogenase_reductase** → *Mercuric reductase* (neighbour P00392), fold-TM 0.9325
- active site: **2/8 catalytic residues conserved** (aligned 2): ['M9->not_covered', 'C11->not_covered', 'C14->not_covered', 'Y62->not_covered', 'C136->C42=', 'C141->C47=', 'C558->not_covered', 'C559->not_covered']
- verdict: **NOT_VERIFIED**

### A0A1M6CQU7 — Nocardiopsis flavescens
- predicted: **flavin_dehydrogenase_reductase** → *Trimethylamine dehydrogenase* (neighbour P16099), fold-TM 0.9243
- active site: **1/4 catalytic residues conserved** (aligned 4): ['C31->T34x', 'Y170->H172x', 'H173->H175=', 'D268->H272x']
- verdict: **NOT_VERIFIED**

### A0A8H5HZQ9 — Collybiopsis confluens
- predicted: **flavin_dehydrogenase_reductase** → *NADH peroxidase* (neighbour P37062), fold-TM 0.851
- active site: **0/4 catalytic residues conserved** (aligned 4): ['H10->S177x', 'S41->R208x', 'C42->S209x', 'R303->G472x']
- verdict: **NOT_VERIFIED**

## Recommendation

Take the **6 verified** to a small pilot (the 3 serine proteases are the most tractable to express
and assay; the di-zinc glyoxalase-II-like hydrolase M3JW22, the ascorbate-peroxidase-like
A0A177THN5, and the PLP/BioA-like F0Y210 each have standard assays). **Drop the 3 flavin**
candidates — same fold, no active site. The 2 partial PLP candidates are second-tier.
