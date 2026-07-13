# Lab Handoff — what to send, and how (2026-06-29)

> **SUPERSEDED — DO NOT ORDER OR SHIP FROM THIS DOCUMENT.** The supporting
> validation and active-site-verification interpretations were corrected on
> 2026-07-13. Rebuild any future handoff under `docs/ATLAS_TRUTH_POLICY.md` with
> a fresh reviewed assay contract, controls, safety review, and exposure entry.

Companion to `docs/lab_pilot_guide_20260629.md` (assays, controls, interpretation).
This file is the **materials + ordering** spec: exactly what to hand a lab or a
gene-synthesis vendor.

## You are not shipping protein — you are shipping designs

You don't have these proteins; nobody does (they're uncharacterized). So the
"thing you send" is an **information packet** plus, optionally, **synthetic genes**
you order and ship to save the lab's cloning time. The physical path is:

> sequence → codon-optimised synthetic gene (vendor) → expression vector →
> express + purify (lab or core) → activity assay (lab/core/you).

## The packet, per target (send all of this)

1. **Identity:** UniProt accession, organism, "uncharacterized protein."
2. **Sequence (FASTA)** — Appendix A below. For multidomain targets, the
   **catalytic-domain boundaries** to express (given below).
3. **AlphaFold model (CIF):** `https://alphafold.ebi.ac.uk/files/AF-<ACC>-F1-model_v6.cif`
   — lets them see the fold and active site.
4. **The prediction:** predicted mechanism, the characterised reference enzyme +
   EC, and the **catalytic residues to confirm** (positions in the sequence).
5. **The assay + controls + success criteria** — from the pilot guide.
6. **Expression notes** (host, tag, signal/pro-peptide handling, solubility risk).

## Recommended FIRST pilot — 3 single-domain targets, 3 different chemistries

Chosen for tractability (single catalytic domain, modest size) and mechanism
diversity, so one round tests the method across oxidoreduction, hydrolysis, and
PLP chemistry.

### 1. A0A177THN5 — heme peroxidase (313 aa, *Tilletia indica*)
- Predicted: class-I-like heme peroxidase; reference **L-ascorbate peroxidase**
  (EC 1.11.1.11). Active-site evidence: 5/5 catalytic residues conserved (distal
  His40, proximal His164, Arg36, Trp180, Asp231 in this protein's numbering).
- **Express:** E. coli, N-/C-His tag; single-domain, no signal peptide to remove.
  Express **apo**, then reconstitute with hemin. Codon-optimise (fungal source).
- **Assay:** ABTS or guaiacol oxidation + H₂O₂ (420/470 nm); confirm heme by Soret
  ~405 nm. Control: omit H₂O₂; positive control = horseradish peroxidase.
- Genuinely dark (locus-tag gene name) → a confirmation here is non-obvious.

### 2. A0A918P095 — serine protease (373 aa, *Streptomyces minutiscleroticus*)
- Predicted: chymotrypsin-clan serine protease; reference **Streptogrisin-B**
  (EC 3.4.21.81). Active-site evidence: Ser321–His204–Asp238 triad with catalytic
  H-bond geometry (2.80 / 2.79 Å).
- **Express:** E. coli — bacterial, easiest host. Sequence has an **N-terminal
  signal + pro-peptide** (~first ~60–80 aa, "MRRRHPAYRG…AAP"): express the **mature
  catalytic domain** (His-tagged) or co-express with pro-region for folding;
  Streptomyces proteases often express in inclusion bodies → refold, or try
  periplasmic secretion.
- **Assay:** Suc-AAPF-pNA (chymotrypsin-like) ± azocasein, 405/440 nm. Control:
  abolition by **PMSF or DFP**; positive control = α-chymotrypsin.
- Genuinely dark (locus-tag) → high-value confirmation.

### 3. F0Y210 — PLP aminotransferase (489 aa, *Aureococcus anophagefferens*)
- Predicted: fold-type-I PLP aminotransferase; reference **adenosylmethionine-8-
  amino-7-oxononanoate aminotransferase (BioA)** (EC 2.6.1.62). Active-site
  evidence: 4/4 conserved incl. **PLP Schiff-base Lys317**.
- **Express:** E. coli, His tag; single-domain. Codon-optimise (algal source).
  Add exogenous **PLP** during expression/assay.
- **Assay:** transamination with an amino-donor/keto-acceptor pair, PLP-aldimine
  signature ~420 nm or 340 nm coupled assay. Control: omit PLP.
- Note: its UniProt gene name is `BIOA` (a **homology-based** guess, not
  experimental) — so this is "less dark" than the other two but the most
  textbook-tractable. Good as the reliability anchor of the trio.

## Second-tier (strong predictions, but need domain-construct design)

- **M3JW22** (di-zinc glyoxalase-II / metallo-β-lactamase, **7/7** catalytic
  residues conserved — the strongest structural prediction) is a **1086 aa
  multidomain/membrane-anchored fusion**; the catalytic di-zinc domain sits near
  the C-terminus (HxHxDH motif ~res 880–900). Express the **isolated metallohydrolase
  domain** (~res ~830–1086), His-tagged, +Zn²⁺; assay S-D-lactoylglutathione
  hydrolysis (240 nm) with **EDTA-abolition** control. High-value but more cloning
  design.
- **A0AAD9KVE2** (tubeworm, 1158 aa) and **A0AA38MP07** (beetle, 641 aa) are
  multidomain proteases — express the **C-terminal trypsin domain** only.

## Ordering, concretely

- **Synthetic genes:** order codon-optimised (for E. coli) constructs from
  **Twist Bioscience / IDT / GenScript**, cloned into a **pET-28a(+)**-type
  His-tag vector. ~$0.1–0.2/bp; each construct is a few hundred dollars and ~1–2
  weeks. For the multidomain ones, order only the catalytic-domain boundary.
- **Substrates/reagents** (commercially available, Sigma/Cayman/etc.): Suc-AAPF-pNA,
  PMSF; ABTS, hemin, H₂O₂; PLP, an amino-donor/keto-acid pair; S-D-lactoylglutathione,
  EDTA.
- **If using a core:** send the FASTA + desired construct boundaries + tag; cores
  will do vector design, expression, and purification for you.

## Appendix A — sequences

(Full FASTA for all six verified targets is in `docs/lab_pilot_targets.fasta`.)
