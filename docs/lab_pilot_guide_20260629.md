# Lab Pilot Guide — Catalytic Earth mechanism atlas (2026-06-29)

A handoff-ready brief for the first wet-lab test of the atlas's mechanism calls.
Written so a bench scientist can act without reading the codebase.

---

## 1. What you are testing, in one paragraph

The atlas predicts an enzyme's **catalytic mechanism** (not just its name) from
structure: it folds a protein with AlphaFold, finds its nearest structural
neighbour in a curated atlas of mechanistically-characterised enzymes (M-CSA),
and — only if the structural match is confident (TM-score ≥ 0.70) — assigns that
neighbour's mechanism. Below the threshold it **abstains**. This pilot asks one
question for each target: **does the predicted catalytic activity actually occur
at the bench?**

## 2. Why now (the evidence behind these picks)

- On an **independent gold benchmark** (experimentally-characterised enzymes,
  labels from EC, never seen by the model), the method recovered the correct
  mechanism for **heme peroxidases 16/16, PLP enzymes 14/16, serine hydrolases
  13/16**, and made **zero confident wrong calls** in any family — every error
  was a safe "I don't know." When it commits, it has been right.
- Each target below additionally passed an **active-site check**: its AlphaFold
  model carries the intact catalytic apparatus (triad geometry or conserved
  catalytic residues), not merely the right fold. Three candidates that had the
  fold but a **degraded** active site were already discarded.
- These are **uncharacterised proteins** (no experimental annotation). A positive
  result is therefore a genuinely new functional assignment — the first
  prospective, gold, off-benchmark confirmation the project could obtain.

## 3. The six targets (all active-site verified)

Fetch each model at `https://alphafold.ebi.ac.uk/files/AF-<ACCESSION>-F1-model_v6.cif`.
"Reference enzyme" is the characterised structural neighbour whose assay applies.

### Tier 1 — most tractable (bacterial/invertebrate serine proteases)
| Target | Organism | Predicted | Reference enzyme | Active-site evidence |
|---|---|---|---|---|
| **A0A918P095** | *Streptomyces minutiscleroticus* | serine protease | Streptogrisin-B (EC 3.4.21.81) | Ser321–His204–Asp238 triad; H-bond geom 2.80/2.79 Å |
| **A0AA38MP07** | *Zophobas morio* (beetle) | serine protease | Chymotrypsinogen A (EC 3.4.21.1) | Ser580–His423–Asp481 triad; 3.22/2.80 Å |
| **A0AAD9KVE2** | *Ridgeia piscesae* (tubeworm) | serine protease | Trypsin (EC 3.4.21.4) | Ser1087–His938–Asp986 triad; 2.99/2.76 Å |

**Assay:** chromogenic peptide hydrolysis (e.g. trypsin-like → BAPNA/Bz-Arg-pNA;
chymotrypsin-like → Suc-AAPF-pNA), 405 nm. **Specificity control:** abolition by a
serine-protease inhibitor (PMSF or DFP). *A. jubatus*-style mammalian zymogens
need activation; bacterial Streptogrisin-type is usually the easiest to express.

### Tier 2 — cofactor enzymes (standard assays, expect to add cofactor)
| Target | Organism | Predicted | Reference enzyme | Active-site evidence |
|---|---|---|---|---|
| **A0A177THN5** | *Tilletia indica* (fungus) | heme peroxidase | L-ascorbate peroxidase (EC 1.11.1.11) | 5/5 catalytic residues conserved incl. distal His, proximal His, Arg, Trp, Asp |
| **F0Y210** | *Aureococcus anophagefferens* (alga) | PLP aminotransferase | adenosylmethionine-8-amino-7-oxononanoate aminotransferase (BioA, EC 2.6.1.62) | 4/4 conserved incl. PLP Schiff-base Lys317 |
| **M3JW22** | *Candida maltosa* (yeast) | di-zinc metallohydrolase | hydroxyacylglutathione hydrolase / glyoxalase II (EC 3.1.2.6) | **7/7** His/Asp di-zinc cluster conserved |

**Assays.**
- **A0A177THN5 (peroxidase):** ascorbate/guaiacol/ABTS oxidation with H₂O₂,
  monitored at 290/470/420 nm; confirm heme by Soret ~405 nm. Reconstitute with
  hemin if expressed apo.
- **F0Y210 (PLP transaminase):** transamination toward the BioA reaction
  (7-keto-8-aminopelargonate ⇌ 7,8-diaminopelargonate using SAM as amino donor);
  generic screen = amino-donor/keto-acceptor pair with PLP, 340 nm coupled assay
  or PLP-aldimine signature ~420 nm. Add exogenous PLP.
- **M3JW22 (glyoxalase II / thioesterase):** hydrolysis of S-D-lactoylglutathione
  (240 nm) or a thioester substrate; confirm metal dependence by Zn²⁺ requirement
  and **EDTA abolition**.

## 4. How to read each outcome

- **Predicted activity detected** → first prospective gold confirmation; record
  kcat/KM if feasible. This is the result that converts the project from
  "validated internally" to "validated in the world."
- **No activity, but protein folds/expresses** → informative negative: either the
  fold-match overreached for that target, or the assay/conditions are off. Note
  which (a misfolded prep is not a model failure).
- **Cannot express/insoluble** → not a model result; substitute the next target.

Run **2–3 targets**, not all six — the Tier-1 serine proteases are the lowest-risk
first experiments. A single clean confirmation is the deliverable.

## 5. Honest scope (what a result does and does not prove)

- These calls are **family/mechanism-class** level (e.g. "serine-protease
  mechanism"), tied to a specific reference enzyme that defines the assay — they
  are not a precise substrate prediction.
- The metal-hydrolase call (M3JW22) is within the atlas's validated fold (MBL/
  glyoxalase-II); the atlas does **not** yet cover metzincin/gluzincin
  metalloproteases, so this pilot does not test those.
- Targets were structurally pre-screened by Pfam fold, so the broad fold is
  expected; the **mechanism-level activity and intact active site** are the novel,
  testable claims.

## 6. Provenance (for the record)

- Candidate generation: `artifacts/v3_gate3_novel_dark_target_shortlist_current702_20260629.json`
- Active-site verification: `artifacts/v3_gate3_active_site_verification_current702_20260629.json`
- Method validation (gold held-out): `artifacts/v3_swissprot_pdbholo_gold_heldout_eval_result_current702_20260629.json`
- Operating point: fold-NN vs the 133-member M-CSA atlas, confidence gate TM ≥ 0.70.
