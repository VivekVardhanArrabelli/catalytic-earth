# SwissProt gold held-out — RESULT (spent once, 2026-06-29)

First **gold** (not bronze) validation of the fold channel **beyond M-CSA**, on a pre-registered,
content-hashed (`54119a7d…`) held-out whose labels come from experimental EC, independent of structure.

## Verdict: PASS (pre-registered aggregate bar)
- In-scope recovery **45/64 = 0.703** (bar ≥ 0.70)
- OOS false-positive **2/72 = 0.028** (bar ≤ 0.40)

## The honest decomposition (more informative than the aggregate)
| family | recovered | abstained | confident misroute |
|---|---|---|---|
| heme_peroxidase_oxidase | **16/16** | 0 | 0 |
| plp_dependent_enzyme | **14/16** | 2 | 0 |
| ser_his_acid_hydrolase | **13/16** | 3 | 0 |
| metal_dependent_hydrolase | **2/16** | 14 | 0 |

**Zero confident misroutes in any family.** Every miss is a safe abstention — when the channel
commits, it is right (45/45 in-scope, 2/72 OOS).

## Read
1. **Recovery generalises off-M-CSA on gold** for heme / PLP / ser_his (**43/48 = 0.90**) — the first
   non-circular, gold, beyond-M-CSA evidence the structural channel works.
2. **Precision/abstention is excellent everywhere** (OOS-FP 2.8%; 0 in-scope misroutes) — the system
   **fails safe**.
3. **metal_dependent_hydrolase is a coverage gap, not a precision failure.** The held-out used EC
   3.4.24 metalloendopeptidases (metzincin/gluzincin fold: MMPs, ADAMs, astacins); the atlas family is
   metallo-β-lactamase-fold-centric, so those folds fall **below** the gate and **abstain** rather than
   miscall. The atlas family is narrower than its name — it is "MBL-fold metal hydrolase."

## Consequence
- The deployable claim widens from "M-CSA only" to **"validated on independent gold for heme, PLP, and
  serine-hydrolase mechanisms, with fail-safe abstention; metal-hydrolase coverage limited to the MBL
  fold."**
- Actionable atlas fix (future): add metzincin/gluzincin representatives to broaden the metal family.
