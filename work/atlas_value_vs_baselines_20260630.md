# Is the atlas real, or reproducible by cheap tools? (head-to-head, 2026-06-30)

Rigorous control on the **independent gold held-out** (136 proteins, EC-derived labels,
independent of structure). Same nearest-neighbour-transfer paradigm, two distance metrics:
**STRUCTURE** (atlas: foldseek TM vs 133 M-CSA members, gate 0.70) vs **SEQUENCE**
(BLAST-like best Smith-Waterman hit among the *same* members). Apples-to-apples.

## Result 1 — accuracy: structure beats sequence transfer
- Atlas (structure) in-scope recovery: **0.70 (45/64)**
- Sequence-NN baseline recovery: **0.41 (26/64)**
- **+0.30 absolute** — mechanism the atlas recovers that pairwise sequence transfer misses.

Stratified by sequence identity to the matched M-CSA entry:

| identity band | n | atlas | sequence-NN |
|---|---|---|---|
| 15–25% | 4 | 0.25 | 0.00 |
| **25–40% (twilight zone)** | 40 | **0.70** | **0.28** |
| 40–100% | 20 | 0.80 | 0.75 |

In the homology **twilight zone (25–40%)** — where sequence transfer becomes unreliable —
the atlas wins ~**2.5×**. At high identity they converge (sequence works there too).

## Result 2 — discrimination / fail-safe: structure separates, sequence can't (the strongest finding)
Out-of-scope set = 72 enzymes outside all covered families (methyltransferase / glycosidase /
isomerase / ligase). Should be abstained on.
- Atlas confident false-positives on OOS: **2/72**.
- But those OOS enzymes have **median 34% sequence identity** to some atlas member (61/72 ≥30%) —
  **as sequence-similar as the in-scope recovered proteins (median 39%).**
- So **sequence identity cannot tell covered from non-covered**; the atlas's structural TM gate can.
  Structure discriminates and abstains where sequence is blind. **This is not reproducible by a
  sequence-NN at any threshold.**

## What is NOT proven (so we don't fool ourselves)
- **Orphan recovery (the strongest claim) is undemonstrated.** 0/45 atlas-recovered proteins were
  sequence-orphans — every one had ≥25% identity to some atlas member (recovered median 37%). So we
  have **not** shown structure assigns mechanism where sequence is *fully* blind; this gold set
  contains ~no orphans. Proving that needs a deliberate <20%-identity / orphan test.
- **Baseline is pairwise (BLAST-like), not a profile HMM.** HMMER/Pfam detect remoter homology and
  could narrow the twilight-zone gap. The discrimination result (Result 2) would likely survive and
  is the stronger claim.

## Verdict
**Not fooling ourselves — the atlas adds real, quantified value over the cheap baseline on two axes
(twilight-zone accuracy, and fail-safe discrimination), and the discrimination advantage is
fundamental, not threshold-tunable.** But the headline "structure sees what sequence can't" is so far
proven for the *twilight* zone, not the *midnight* (orphan) zone. The two follow-ups that would close
it: (1) re-run the baseline as HMMER/Pfam; (2) deliberately test sequence-orphan structural matches.
