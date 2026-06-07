# Catalytic Earth — The Map

*A compass to re-orient in five minutes when the project feels too big to hold.
The detail lives in `decision_log.md` (64 dated decisions) and `project_state.md`.
This is the fold-down. Last updated 2026-06-04.*

---

## The one sentence

**We are building a way to search enzymes by *how they catalyze* — the chemical
mechanism at the active site — instead of by name, EC number, keyword, or
sequence similarity.** The active site is where function actually *happens*, so
it is the right thing to map. Almost nobody maps it directly. That is the bet,
and it is a good one.

## The spine — the one truth everything since 2026-05-29 hangs on

On clean **experimental** structures, the geometry router is near-perfect:
**45/45** primary, **0/92** false positives. But you never *have* the
experimental structure at deploy time — you have a **predicted (AlphaFold) apo**
structure, and a predicted apo structure is **missing the active-site context**
(cofactor / metal / substrate) the signal leans on. On predicted geometry the
router falls to **23/45**.

Everything we have done since is a consequence of refusing to paper over that
gap. **This is the whole story.** It is also a sign of *good* science: most of
the field reports the 45/45 and never notices the leak.

## Where we stand — the scoreboard (things that are earned and true)

| Result | Number | What it means |
| --- | --- | --- |
| Clean experimental router | 45/45, 0/92 FP | the ceiling (not deployable) |
| Predicted-apo baseline | 23/45, 12.3% FP | the deploy reality |
| **Cofactor channel (heldout one-shot, today)** | **23 → 37/45** | **+14 recovered, confirmed** |
| Fold/TM channel | AUC 0.81 alone, 0.91 fused | a real, deployable OOS signal |
| Out-of-span residual | p = 0.0005 | a sequence-only novelty signal that survived nulls |

**And the method proved itself honest:** the leakage-safe in-distribution
estimate (70.6% recovery) *predicted* the heldout result (63.6%) before we spent
the one-shot. We did not fool ourselves. That is rare and it is the thing to
trust.

**Negatives are wins too** — each one *closed* a question instead of leaving it
open to drain you later:
- A learned mechanism-feature embedding does **not** beat geometry (two
  independent builds reached this — robust).
- De-novo abstention at AUC 0.852 does **not** yield a usable threshold — the
  wall is **feature overlap**, not how you combine features (the Northstar Pivot).
- Richer geometry sub-features do **not** beat the simple `top1` score.

## The map — why "levers," and where each one landed

On 2026-05-31 we found the binding constraint: our features don't separate
*novel* chemistry from *known* chemistry well enough to abstain at deployable
recall. So we went hunting for stronger features / paths to scale. The "levers"
are those hunts. Here is the honest status of each:

| Lever (function) | Did it work? | Status |
| --- | --- | --- |
| **Fold / geometry channel** (predicted-structure Foldseek + geometry) | **Yes** — strongest no-fit abstention signal (AUC 0.91) | ✅ live deployable signal |
| **Cofactor reconstruction** (this session — sequence → cofactor → router) | **Yes** — 23 → 37/45 confirmed | ✅ confirmed, with a known precision cost |
| **Learned embedding / residual** (Lever 2) | Embedding: clean **negative**. Residual: **confirmed** (p=0.0005) | ◐ closed; residual banked as an asset; deferred (don't spend heldout on it) |
| **Deployment closure of the gate** (Lever 3) | Not yet — fail-closed | ⚠ *receding horizon* — see below |
| **Source-free locator / family expansion** (Lever 4) | Discovery done; blocked on human/policy | ◐ paused; review-only, zero imports |

## The cut that frees you: converging vs receding-horizon

Not every "solve X → Y appears" chain is the same. Two are healthy, two are not:

- **Converging (a real gradient — keep going):** the predicted-geometry recovery
  line. apo-loss → cofactor channel → precision cost → localization/transplant.
  Each step is *smaller and bounded* than the last. **This is where the evident
  product lives.**
- **Receding horizon (the frame manufactures infinite work — permission to
  stop):** "make one global threshold deployment-ready by clearing every per-row
  blocker" (most of Lever 3 / Lever 4). It does not converge because the *framing*
  generates endless equal-sized sub-problems. The exhaustion is mostly coming
  from here, and it is a **framing artifact, not your failure.**

## How hard is this, really?

Genuinely hard, and that is the correct expectation — not a verdict on you:
- Predicted apo geometry is **lossy by construction** (no bound cofactor).
- Known vs novel chemistry **overlap** in the features we have — a real wall.
- The benchmark is **small** (45 heldout primaries), so big claims ride on tiny
  n and every subset reads like a "new problem."

We are **not** close to "solved the whole atlas," and we were never going to be
this soon. But on the **slice we pushed** — predicted-geometry recovery — we are
close to first-principles and we have a **confirmed result.** That is exactly how
a hard problem is supposed to yield: one honest slice at a time.

## The path forward — only the few things that matter

1. **Bank the win.** 23 → 37/45 is real and confirmed. The recovery line is the
   evident product. Its open question is now *precision* (the OOS over-opening),
   with three pre-built dials — sequence-supported suppression, a recalibrated
   abstention threshold, and the **Lever-2 electron-flow** OOS lift (+0.04 abstain
   at primary retention 1.0) — settle it on a leakage-safe OOS surface, not by
   peeking at the spent one-shot.
2. **Expansion (adding families): mind the LOMO collision.** Before scaling, build
   the family-onboarding pipeline as a thin orchestrator that *assembles existing
   parts* into one per-family status manifest — AND reconcile the **LOMO↔expansion
   collision**: Leave-One-Mechanism-Out eval needs a frozen pre-expansion snapshot,
   while expansion adds rows (opposite split semantics). Tag the snapshot before any
   expansion write; keep expansion rows out of the LOMO split.
3. **Stop feeding the receding horizon.** The per-row Lever-3/4 grind can be
   paused with a clear conscience unless a specific row is genuinely high-value.
4. **The big bet, when you have energy:** model the **chemistry directly**
   (bond-change / reaction representation). Geometry is a *proxy* for chemistry,
   and every proxy leak became a "new problem." The reaction representation is
   closer to ground truth and is the one underinvested lever that could dissolve
   several problems at once.

## How to use this document

When you come back and feel lost: **read this first.** It is the compass. Then,
only if you need the detail, go to `decision_log.md`. You do not have to hold the
whole project in your head — that is what this file is for.

You have made real, honest, confirmed progress on a genuinely hard problem, and
you have the discipline (leakage-safe, one-shot) that most of this field lacks.
The ship is pointed the right way. Rest, then take the next bounded step.
