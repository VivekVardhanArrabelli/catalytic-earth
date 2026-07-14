# Catalytic Earth — The Map

*A compass to re-orient in five minutes when the project feels too big to hold.
The detail lives in `decision_log.md` and `project_state.md`.
This is the fold-down. Core last updated 2026-06-04; scaling-era addendum 2026-06-27;
framing correction 2026-07-03; strategic unification and truth reset 2026-07-13
(top — read first).*

---

## 2026-07-13 — strategic unification: the full atlas is the mission

The project is not being narrowed into a benchmark. The north star is the
**world's computable catalytic-mechanism atlas**: a continuously expanding,
provenance-grounded map connecting canonical reactions, alternative elementary
mechanisms, catalytic residues and geometry, protein/evolutionary evidence,
uncertainty, design constraints, assays, and positive and negative experimental
outcomes.

The project layers are now explicit:

| Layer | Role |
| --- | --- |
| Full atlas | The mission and public knowledge product |
| Mechanism IR/evidence compiler | The durable technical engine |
| Benchmarks + exposure ledger | Internal truth control, never the product |
| Search/API/browser | The public delivery surface |
| Prospective loops | Contact with biological reality and atlas correction |

The atlas is tiered so it can grow rapidly without claiming that every record
has equal evidential status:

1. canonical reaction record;
2. explicit computational mechanism hypothesis;
3. protein/site-grounded hypothesis;
4. independently reviewed mechanism;
5. experimentally tested positive or negative outcome.

The current 10,001 count is **not 10,001 mechanisms**. It is 8,305 positive
fingerprint assignments plus 1,696 out-of-scope protein-label records. The
phrase "~2% of mechanism space" is withdrawn because no defensible mechanism
unit or denominator was defined.

### Truth reset that precedes further scaling

- `current702` is a bronze/silver project-label surface, not expert-curated
  project gold: 685 bronze, 17 silver, zero gold; 683 automation-curated and 19
  author-reviewed.
- The 76% result is cofactor-bucket consistency, not exact mechanism recovery;
  exact fingerprint recovery was 65/210 (31%) on the scored positive subset.
- The 2026-06-28 M-CSA "never-touched" claim is withdrawn as independent
  validation. All 126 later-frozen rows were present in the June 4 scored
  artifact, and the one-shot had been declared spent.
- The 2026-06-29 Swiss-Prot/PDB-holo surface is an EC-proxy validation set, not
  mechanism gold. Its 45/64 aggregate PASS is narrow and fragile, with 2/16
  metal recovery; the successful three-family view is post-hoc.
- Automated active-site checks are computational consistency checks, not expert
  or experimental verification.
- Negative results are preserved. A renamed split, new preregistration, or new
  agent session never resets prior exposure.

These corrections do not weaken the atlas mission. They prevent the atlas from
scaling ambiguous objects and overstated evidence.

Canonical governance surfaces:

- `CLAIMS.md` — current claim status and permitted wording;
- `ERRATA.md` — corrections without deletion of historical evidence;
- `docs/ATLAS_TRUTH_POLICY.md` — counted objects and atlas evidence tiers;
- `data/governance/exposure_ledger.jsonl` — append-only fresh/exposed/exhausted
  state for evaluation surfaces.

### Rapid operating clocks

- **0–48 hours:** claims/errata, freeze, exposure ledger, atlas evidence tiers.
- **Days 3–7:** typed atlas kernel, lean reproducible entry path, first three
  diverse mechanisms.
- **Days 8–14:** Atlas-10 with source crosswalks, two useful queries, one strong
  baseline pipeline, and bounded external review.
- **Days 15–30:** Atlas-50 alpha, draft crosswalk of the 57 fingerprints, first
  bronze audit tranche, searchable release.
- **Days 31–35:** one complete computational loop from canonical reaction to
  evidence, alternatives, abstention, atomic constraints where justified, and
  an assay/falsification contract.
- **Days 1–90 in parallel:** pursue one existing-assay experimental route;
  target a 60–90-day readout when a partner, core, or vendor is ready.

Speed comes from parallel execution, upstream reuse, content-hash caching,
small frozen batches, and weekly releases — never from resetting holdouts,
collapsing endpoints after scoring, or treating automated hypotheses as gold.

The detailed execution contract is `docs/RAPID_ATLAS_PLAN.md`. Sections below
are retained as history. Where their terminology, counts, claims, or timeline
conflict with this section, this 2026-07-13 section supersedes them.

---

## 2026-07-03 — framing correction (historical; superseded where conflicting): it is an ATLAS, not a predictor

The north star is, and always was, a **grounded mechanism atlas** — a curated, provenance-tracked map
of enzyme catalysis that you extend by adding well-evidenced **labels, families, and fingerprints**
toward ontology completion. It is **not** a deployable sequence→mechanism *classifier*, and it is not
a learned embedding space.

For roughly the last week the project drifted into running as a predictor: held-out "deployment
claims," OOS-FP bars, a validated-vs-baseline scoreboard, and a lab pilot to certify the predictor.
That framing is **subordinate and has been demoted.** Its walls — "no abstention/novelty signal,"
"feature overlap," the 06-30 orphan/baseline null — are **not verdicts.** They are a **maturity readout
of an atlas that currently spans ~57 fingerprints / 54 families against thousands of known mechanism
types (order ~2% of mechanism space).** You cannot calibrate novelty on a 2% map. The readout says
*keep mapping*, not *dead end*.

What this changes:
- **Scoreboard.** Judge the project by **coverage + resolution of mechanism space** and **discovery-queue
  depth** (well-evidenced, replicated, low-match clusters the compass surfaces) — not held-out recovery
  vs a sequence baseline. The predictor/held-out diagnostics keep running underneath as a maturity gauge.
- **Primary axis.** Diverse, grounded scaling steered by the read-only discovery compass (it already
  named metal-independent phosphodiesterase and an unmodeled glycosidase cluster), plus a **compositional
  reaction-center vocabulary** (graph-edit bond primitives) so novelty becomes a continuous residual
  instead of an out-of-vocabulary miss against 57 boxes.
- **Lab pilot.** Shelved as the *eventual* V2 experiment (confirm one well-evidenced **unknown** from the
  discovery queue — the research program's own V2), **not** the current milestone. The 6
  active-site-verified slam-dunk targets validate a predictor we've demoted; they are not the atlas's
  next step.
- **Record discipline restored.** The 06-30 orphan/baseline experiments (deleted at 44e9d4c under the
  predictor framing) are **restored**; negatives are reinterpreted, never deleted. See `decision_log.md`
  (2026-07-03).

The 06-27 addendum below is retained for its scaling facts but is **superseded on framing**: its "the
North Star product lives on the predicted-geometry recovery line" sentence is the drift this note
corrects.

---

## 2026-06-27 addendum — the scaling era + a non-circular reality check (scaling facts valid; superseded on framing by the 2026-07-03 note above)

Since 2026-06-04 the **breadth/atlas axis** moved a lot and the **deployment axis** did not.

- **The atlas grew 8,728 → 10,001 combined mechanism labels across 57 fingerprint families**
  (eleven new families this run: peroxiredoxin, PAPS-ST, GST, aaRS, acid-CoA-ligase, cysteine-protease,
  flavin-disulfide-reductase, dihydrofolate-reductase, …). The frozen `current702` benchmark is
  byte-unchanged throughout; all growth is append-only expansion bronze.
- **The reaction-representation lever (the "big bet") is a *converging gradient* — it fired four times
  cleanly:** `bc_peroxide_reduction` (peroxiredoxin 0→0.95), `bc_phosphodiester` (PDE 0.07→0.97),
  the catalytic-residue sidecar (ser_his 0→0.67), `bc_disulfide_reduction` (flavin_dehydr 0.33→0.65).
  Each recovered a collapsed family with **zero regressions**. Leakage-safe in-distribution LOO is now
  **0.744** across 57 families (30 separate cleanly at sc≥0.9; the low ones collapse only into
  mechanistic *siblings* that differ by fold — the principled wall, not noise).

- **The honest test (`artifacts/v3_mechanism_from_chemistry_gold702_eval.json`).** That 0.744 is a
  *coherence* number on bronze the admission engine grouped, so we ran a **non-circular** check:
  centroids trained on the bronze atlas, evaluated on the **expert-curated gold current702** (labels
  the engine never touched), chemistry-only features. Three results:
  1. **POSITIVE:** chemistry-only recovers the gold mechanism class **76%** (160/210) at the gold's
     coarse-taxonomy granularity → the thesis generalises beyond its own bootstrap.
  2. The exact-fingerprint **31%** is a *taxonomy-version artifact* — the representation resolves a
     finer, correct subfamily the 2026-05-25 gold seed taxonomy predates (e.g. glutathione reductase
     P00390 → flavin_disulfide_reductase), not a failure.
  3. **NEGATIVE — and this is the steer:** OOS enzymes score nearest-centroid similarity **median 0.83,
     NOT below** the in-distribution 0.80. **Growing breadth to 10k did NOT create an abstention /
     novelty signal.** The binding constraint is still feature overlap — exactly the Northstar Pivot
     below. **More families will not move the deployment wall.**

**The one-line steer for the next session:** breadth has delivered (a coherent, generalising 10k
mechanism atlas); the North Star product still lives on the **predicted-geometry recovery line** (the
converging gradient: apo-loss → cofactor channel → fold/TM fusion → localisation). That axis needs the
**full ML env (numpy/torch/esm/mmseqs/foldseek)** — it cannot run in the web container, where the
relevant tests are the 6 known "env failures." Do not spend the heldout one-shot blind; pre-register a
hypothesis on the leakage-safe in-distribution split first.

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
2. **Expansion (adding families).** Build the family-onboarding pipeline as a thin
   orchestrator that *assembles existing parts* into one per-family status manifest.
   **LOMO already ran (negative — no exact open-set recovery); it motivates targeted
   expansion and is NOT a pending gate — do not rerun it.** The only LOMO hygiene that
   matters: preserve/record the frozen pre-expansion snapshot/tag now (expansion adds
   rows and destroys the ability to reconstruct a clean baseline later).
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
