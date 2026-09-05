# Gate 3 — Novel (uncharacterized) lab-target shortlist (2026-06-29)

> **2026-09-05 correction — A0A177THN5:** the APX-specific transfer from
> P48534 is withdrawn, and the larger APX-versus-CcP study is retired.
> CcP-like is a provisional working interpretation, not demonstrated activity.
> See [CE-017 and the public-source reassessment](../docs/COMPUTATIONAL_REVIEW_20260905.md).

Fold channel run over **genuinely uncharacterized** proteins (unreviewed, named "Uncharacterized
protein", no EC, predicted/inferred existence) carrying an atlas-family Pfam. Each is folded
(AlphaFold) and matched by foldseek (exhaustive, exact TM) to the 133-member M-CSA atlas; calls
retained at **TM >= 0.70** (the high-precision gate: 24/25 = 0.96 on the M-CSA baseline).

**Pool 326 → 239 confident calls.** By family: {'metal_dependent_hydrolase': 1, 'ser_his_acid_hydrolase': 61, 'heme_peroxidase_oxidase': 47, 'plp_dependent_enzyme': 62, 'flavin_dehydrogenase_reductase': 68}.

## Honest scope
> These are genuinely uncharacterized proteins (no experimental EC, no informative name). The fold channel matches each to a characterized M-CSA enzyme at TM>=0.70, yielding a mechanism-class call + the nearest characterized enzyme (which defines the assay). The Pfam prefilter means the broad fold is already implied; the fold/atlas step adds (a) confirmation the AlphaFold model adopts the catalytic fold, (b) a quantitative structural confidence, (c) the specific characterized neighbour and its assay. A positive bench result is the first GOLD off-M-CSA label; it also feeds Gate 2.

Unlike the earlier off-M-CSA list (all already-characterized Swiss-Prot), **these have no
experimental function** — a bench result here is a genuine first gold off-M-CSA label, not a re-confirmation.

## Metal-dependent hydrolase (`metal_dependent_hydrolase`)

- **M3JW22** — Candida maltosa (strain Xu316) (Yeast)  · 1086 aa · existence: Inferred from homology
  - predicted mechanism: **metal_dependent_hydrolase**; nearest characterized enzyme: Q16775 *Hydroxyacylglutathione hydrolase, mitochondrial* (EC 3.1.2.6) at fold-TM **0.8552**
  - assay: di-metal hydrolase assay (phosphoester/thioester/beta-lactam hydrolysis per neighbor); Zn2+/metal dependence + EDTA abolition.

## Ser/His hydrolase (`ser_his_acid_hydrolase`)

- **A0AAD9KVE2** — Ridgeia piscesae (Tubeworm)  · 1158 aa · existence: Predicted
  - predicted mechanism: **ser_his_acid_hydrolase**; nearest characterized enzyme: P35049 *Trypsin* (EC 3.4.21.4) at fold-TM **0.9394**
  - assay: Ser/His triad hydrolysis (ester/amide/peptide); active-site Ser inhibitor (PMSF/DFP) abolition.

- **A0AA38MP07** — Zophobas morio  · 641 aa · existence: Predicted
  - predicted mechanism: **ser_his_acid_hydrolase**; nearest characterized enzyme: P00766 *Chymotrypsinogen A* (EC 3.4.21.1) at fold-TM **0.9255**
  - assay: Ser/His triad hydrolysis (ester/amide/peptide); active-site Ser inhibitor (PMSF/DFP) abolition.

- **A0A918P095** — Streptomyces minutiscleroticus  · 373 aa · existence: Inferred from homology
  - predicted mechanism: **ser_his_acid_hydrolase**; nearest characterized enzyme: P00777 *Streptogrisin-B* (EC 3.4.21.81) at fold-TM **0.9244**
  - assay: Ser/His triad hydrolysis (ester/amide/peptide); active-site Ser inhibitor (PMSF/DFP) abolition.

## Heme peroxidase/oxidase (`heme_peroxidase_oxidase`)

- **A0A177THN5** — Tilletia indica  · 313 aa · existence: Inferred from homology
  - predicted mechanism: **heme_peroxidase_oxidase**; nearest characterized enzyme: P48534 *L-ascorbate peroxidase, cytosolic* (EC 1.11.1.11) at fold-TM **0.9515**
  - assay: peroxidase dye oxidation / H2O2 turnover; heme Soret ~405 nm confirmation.

## PLP-dependent enzyme (`plp_dependent_enzyme`)

- **A0AAD6NFH7** — Drechslerella dactyloides (Nematode-trapping fungus) (Arthrobotrys dactyloides)  · 262 aa · existence: Predicted
  - predicted mechanism: **plp_dependent_enzyme**; nearest characterized enzyme: P24630 *Glutamate-1-semialdehyde 2,1-aminomutase* (EC 5.4.3.8) at fold-TM **0.8823**
  - assay: PLP-dependent turnover (transaminase/decarboxylase per neighbor); 420 nm aldimine; PLP dependence.

- **F0Y210** — Aureococcus anophagefferens (Harmful bloom alga)  · 489 aa · existence: Inferred from homology
  - predicted mechanism: **plp_dependent_enzyme**; nearest characterized enzyme: P12995 *Adenosylmethionine-8-amino-7-oxononanoate aminotransferase* (EC 2.6.1.62) at fold-TM **0.9735**
  - assay: PLP-dependent turnover (transaminase/decarboxylase per neighbor); 420 nm aldimine; PLP dependence.

- **B3NHH6** — Drosophila erecta (Fruit fly)  · 494 aa · existence: Inferred from homology
  - predicted mechanism: **plp_dependent_enzyme**; nearest characterized enzyme: P16932 *2,2-dialkylglycine decarboxylase* (EC 4.1.1.64) at fold-TM **0.9358**
  - assay: PLP-dependent turnover (transaminase/decarboxylase per neighbor); 420 nm aldimine; PLP dependence.

## Flavin dehydrogenase/reductase (`flavin_dehydrogenase_reductase`)

- **A0A8H5HZQ9** — Collybiopsis confluens  · 1106 aa · existence: Predicted
  - predicted mechanism: **flavin_dehydrogenase_reductase**; nearest characterized enzyme: P37062 *NADH peroxidase* (EC 1.11.1.1) at fold-TM **0.851**
  - assay: NAD(P)H oxidation at 340 nm coupled to electron-acceptor reduction; FAD/FMN cofactor confirmation.

- **A0A1R2B242** — Stentor coeruleus  · 445 aa · existence: Inferred from homology
  - predicted mechanism: **flavin_dehydrogenase_reductase**; nearest characterized enzyme: P00392 *Mercuric reductase* (EC 1.16.1.1) at fold-TM **0.9325**
  - assay: NAD(P)H oxidation at 340 nm coupled to electron-acceptor reduction; FAD/FMN cofactor confirmation.

- **A0A1M6CQU7** — Nocardiopsis flavescens  · 652 aa · existence: Inferred from homology
  - predicted mechanism: **flavin_dehydrogenase_reductase**; nearest characterized enzyme: P16099 *Trimethylamine dehydrogenase* (EC 1.5.8.2) at fold-TM **0.9243**
  - assay: NAD(P)H oxidation at 340 nm coupled to electron-acceptor reduction; FAD/FMN cofactor confirmation.

