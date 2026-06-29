# SwissProt + PDB-holo gold held-out — pre-registration (2026-06-29)

The **last non-lab validation rung**: an independent gold held-out *beyond* M-CSA.

- **Label independence:** true family is mapped from each entry's **experimentally-supported EC**
  (reviewed Swiss-Prot, evidence at protein level) via a fixed unambiguous EC→family table. The
  predictor (fold-NN vs the 133-member M-CSA atlas) never sees the EC — so scoring is non-circular.
- **Disjoint:** excludes all M-CSA UniProts (996), the atlas (133), and every prior dev pool
  (off-M-CSA bronze, dark pool, novel pool, download manifest) — 1,839 exclusions total.
- **Frozen set:** 136 rows — 64 in-scope (16 each: ser_his, metal hydrolase, heme peroxidase, PLP)
  + 72 OOS (18 each: methyltransferase, glycosidase, isomerase, C–N ligase). sha256
  `54119a7deb70fe0a933669100b8ca187d58eae218dcba53b44d63599c0438f3d`.
- **Frozen rule:** fold-NN nearest neighbour vs atlas, gate TM ≥ 0.70; in-scope recovered iff
  fold-NN family == true family AND TM ≥ 0.70; OOS false-positive iff TM ≥ 0.70 (a confident
  covered call on an out-of-scope enzyme).
- **Pre-committed bar:** in-scope recovery ≥ 0.70 AND OOS-FP rate ≤ 0.40 (mirrors the spent M-CSA
  one-shot, which passed at 0.745 / 0.190).
- **flavin excluded from in-scope:** no unambiguous EC signature, and it failed active-site
  verification — kept out to keep the set pristine.

Spend protocol: fetch AlphaFold structures → foldseek vs atlas → apply the frozen rule → compare to
the frozen bar **once**; do not alter rows/rule/bar after reading any score.
