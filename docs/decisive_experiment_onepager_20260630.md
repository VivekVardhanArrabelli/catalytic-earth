# The Decisive Experiment — one pager (2026-06-30)

## What we have shown so far (measured, not asserted)
- **Validated beyond its benchmark.** On an independent gold held-out (labels from experimental EC, *independent of structure*), the atlas recovers mechanism for heme 16/16, PLP 14/16, serine 13/16, with **zero confident misroutes** — it **fails safe**.
- **Beats the cheap baseline.** Same nearest-neighbour paradigm, structure vs. sequence: atlas **0.70** vs. sequence-transfer **0.41**; in the homology twilight zone (25–40% identity) **0.70 vs 0.28 (~2.5×)**.
- **Discriminates where sequence can't.** Out-of-family enzymes are *as sequence-similar* to the atlas as in-family ones (34% vs 39%), yet the atlas abstains on 70/72 — a separation no sequence threshold achieves.
- **Orphan capability — existence proof only.** Where structure is confident on a sequence-orphan (<25% identity), it was correct **2/2**; but such orphans are **0.6% (7/1139)** of *characterizable* enzymes. The unique "structure where sequence is blind" power is real but thinly evidenced where we can check it — its scope is the **dark proteome**, where ground truth doesn't yet exist.

**Honest bottom line:** the atlas is *not* reproducible by cheap tools (accuracy + fail-safe are real), but its singular claim — annotating proteins nobody else can — is a 2-case existence proof. The lab is the only way to extend it into the zone where it matters.

## The experiment: one dark + sequence-orphan + atlas-confident protein
**Target profile** (the intersection of everything proven):
1. **Dark** — uncharacterized: no EC, no experimental function. *(So the answer exists nowhere; the lab is the first ground truth.)*
2. **Sequence-orphan** — <25% identity to any atlas member *and* no significant BLAST/Pfam hit. *(So sequence methods are blind.)*
3. **Atlas-confident** — foldseek TM ≥ 0.70 to an atlas member, active-site residues verified. *(So the atlas makes a specific, falsifiable mechanism call.)*
4. **Tractable** — single-domain, E.-coli-expressible, standard assay.

**The prediction tested is the atlas's, not Claude's.** It is produced mechanically by foldseek-vs-atlas + the validated TM gate + fingerprint transfer, and it is *specific*: a named mechanism, the structural neighbour, and the catalytic residues/positions — a falsifiable claim an LLM cannot fabricate for an orphan.

## What makes this a test of the atlas — not of cheap tools or an LLM (the critical control)
**Before the assay, we pre-register (timestamped) the prediction of every competitor on this exact sequence, and the experiment only proceeds if they all fail:**
- **BLAST / HMMER / Pfam** → must be silent or non-committal.
- **A protein language model (ESM-family function head)** → must abstain or disagree.
- **A frontier LLM given the bare sequence, blinded** (no name/organism) → must fail or disagree.
- **The atlas** → makes a confident, specific mechanism call.

If any baseline already gets it, **we discard that target and pick another** — a confirmation there wouldn't isolate the atlas. Only when *the atlas commits and every cheaper method (including the LLM) is silent or wrong* does the wet assay adjudicate. A positive result is then attributable to the atlas alone. *(Gating condition: if no such target can be found, that is itself the finding — the atlas adds no isolable capability — and we do not spend on the lab.)*

**Wet readout:** differential-diagnostic assay for the predicted mechanism (e.g. activity + the predicted catalytic-class inhibitor / cofactor dependence), so the result confirms the *specific mechanism and residues*, not a vague label.

## What the result reveals
- **Positive** → first evidence the atlas assigns *correct, mechanism-level function* to a protein that **no existing method and no database could** — the unique capability, demonstrated where it actually matters (the dark proteome). This is the north-star claim, earned.
- **Negative** → the confident-orphan call overreached; bounds the capability to the twilight zone. Still informative, and cheap to have learned from one experiment.

## How we use the result
- **Positive:** it is the proof point that justifies scaling (run the atlas across the dark proteome to mint a prioritised list of novel mechanism annotations) and the asset that unlocks collaboration/funding — a measured, baseline-beating, lab-confirmed capability, not a benchmark argument.
- **Negative:** redirect to the atlas's *proven* value — accurate, abstaining, searchable mechanism transfer in the twilight zone — and invest in broadening the atlas (more gold families) rather than the orphan claim.

## Immediate next step (free, compute-only)
Run the atlas over a **sequence-orphan dark pool** (no Pfam family match) to find the target satisfying profile (1)–(4), then build the pre-registered baseline panel. Finding it — or failing to — is the next decision point, before any spend.
