# Raw-Fusion FP Attribution (predicted-geometry heldout)

Read-only re-derivation from persisted audits. No production scoring, threshold,
label, or registry change.

## Question (Step 1 fork)

Does the raw-fusion false-positive leak skew toward OOS rows or wrong primary calls?
This forks the plan: OOS-concentrated -> concordance gating is the fix;
wrong-primary-concentrated -> chase a specific cofactor source instead.

## Result

| Regime | primary correct | primary wrong | OOS/sec FP (rate) |
| --- | ---: | ---: | ---: |
| Original hand router (no fusion) | 23/45 | 5 | 10 (0.123) |
| Raw fusion | 31/45 | 13 | 46 (0.568) |

- Raw-fusion confident-wrong split: **46 OOS vs 13 wrong-primary = 78% OOS-concentrated**.
- Incremental leak fusion introduced over baseline: **+36 OOS FP, +8 wrong-primary**
  (buying +8 correct recoveries). The marginal leak is **82% OOS** (36 of 44).

## Verdict

**OOS-concentrated -> concordance gating is the indicated fix.** OOS rows match no
fingerprint skeleton well on geometry, so requiring the geometry channel to second a
cofactor fire should collapse the OOS leak while keeping corroborated recoveries (where
a dehydrogenase-like geometry and a flavin call agree). The residual ~8-row incremental
wrong-primary leak is the target for **class-conditional cofactor trust**: lean on metal
(M-Ionic AUC 0.781); discount weak organic-cofactor calls (heme trained on 18 examples,
AP ~0.53).

## Limitation (honest)

A per-fingerprint breakdown of the 46 OOS / 13 wrong-primary FP is not re-derivable in
this environment: the full per-row raw_fused route was not persisted (only the five named
target rows + aggregate masks), and the cofactor channel cannot be rebuilt here (no
numpy/sklearn; ESM embeddings absent; rebuild needs a disallowed large download). The
aggregate split is unambiguous and settles the fork.
