# Predicted-Geometry Robustness Pipeline — Runbook

How to make the mechanism router robust to predicted (apo) active-site geometry,
and how to onboard a **new family / new missing-context type** into the same
pipeline. The pipeline is family-agnostic; the cofactor channel is one
instantiation of it (the demonstrated case).

## The problem this solves

The router scores active-site geometry. Experimental structures are **holo**
(cofactor / metal / substrate bound). AlphaFold / ESMFold structures are **apo by
construction** — they never predict the bound context. So a router validated on
holo geometry degrades when deployed on sequence -> predicted structure. For the
current v1 families the drop is clean experimental 45/45 -> AlphaFoldDB predicted
23/45 primary, and the decomposition shows it is **100% cofactor-loss, 0%
backbone/fold**.

General problem statement: **reconstruct the deploy-missing active-site context
from sequence, and abstain when you cannot.**

## The pipeline (four steps, all generic)

1. **Diagnose** which deploy-missing context causes the drop, per family.
   - Compare experimental vs predicted-apo geometry on rows you can score
     leakage-safe. Classify each lost primary by *what is missing*
     (cofactor / metal / substrate / PTM / interface / disulfide ...).
   - Module: `predicted_geometry_robustness.build_*` decomposition helpers.
   - **Do not assume cofactor loss.** A new family may lose something else, or
     nothing (e.g. a serine-hydrolase triad carries no cofactor and survives apo
     prediction natively — the correct action there is "reconstruct nothing").

2. **Bound** the ceiling: if that context were restored, how many primaries come
   back? This is the upper bound any reconstruction can reach.
   - Restoration probe (inject the *experimental* context onto the predicted
     backbone — an oracle, not deployable) + graft-fidelity probe.

3. **Reconstruct** the context from sequence — leakage-safe.
   - Build a `sequence -> <context> presence` channel. **Supervise it with a
     STRUCTURAL observation only** (e.g. `ligand_context.cofactor_families`, or a
     locus sidecar) — never the mechanism fingerprint, EC, Rhea, mechanism text,
     or the benchmark label (that would be circular / leaky).
   - Fit heads on the **train** split; select thresholds/backend on the
     **calibration** split; never read heldout. Reference implementation:
     `cofactor_presence_calibration.py` (CLI
     `build-cofactor-presence-calibration`).
   - Emit a per-entry `channel_predictions` surface (the schema the harness
     consumes): each row has `entry_id`, `predicted_<context>_families`,
     `prediction_sources`, `scores`.

4. **Fuse + abstain**: inject the reconstructed context into the router where the
   experimental context used to plug in, and abstain where reconstruction is
   unsure.
   - Reference: `predicted_geometry_recovery.py` (CLI
     `build-in-distribution-predicted-geometry-recovery`). It scores the router
     three ways per in-distribution row — experimental, predicted-apo, and
     predicted-apo + injected channel — and reports the recovery.

## Why the in-distribution harness is the development surface

The 45->23 number is **heldout**, and the heldout read is **one-shot**. The
harness reproduces the same degradation-and-recovery question on
**in-distribution** rows (never the benchmark), so you can iterate to convergence
without spending the one-shot. The router classifies against the eight mechanism
fingerprint templates (no per-row self-match), so the experimental-minus-apo and
fused-minus-apo *deltas* are meaningful even though absolute in-distribution
accuracy is optimistic.

**Honesty rule:** the channel is fit on the train split, so its predictions are
in-sample for train rows. Headline recovery on the **calibration** rows
(out-of-sample for the channel); report train only as an in-sample reference.

Demonstrated cofactor result (calibration, out-of-sample, 35 rows, threshold
0.4115): experimental 34/35 -> predicted-apo 17/35 -> cofactor-fused 30/35,
recovering 12/17 apo-lost primaries (70.6%) with 0 regressions.

## Onboarding a NEW family / context — step by step

1. **Add the family to the atlas** (fingerprint template + in-distribution rows
   with that `fingerprint_id`). The harness auto-includes any in-distribution row
   with a non-null fingerprint and an atlas structure.

2. **Diagnose (step 1 above).** Run the failure decomposition for the new family.
   Identify the dominant missing context. If the drop is small / not
   context-loss, stop — no reconstruction needed.

3. **Confirm two preconditions exist:**
   - a **structural observation** in the experimental features to supervise the
     channel leakage-safe (cofactors: `ligand_context.cofactor_families`; the
     locus sidecars already extend to cobalamin / radical-SAM / iron-sulfur). If
     none exists, materialize one first (structural only).
   - a **router hook that consumes that context.** Cofactors have the 0.18
     `cofactor_context_score` term in `geometry_retrieval.score_entry_against_fingerprint`.
     A new context type (substrate, PTM, interface) needs an analogous scoring
     term before fusion can move the score.

4. **Build the reconstruction channel** of the same shape as
   `cofactor_presence_calibration` (train-fit / cal-threshold / no heldout),
   emitting `channel_predictions` with `predicted_<context>_families`.

5. **Write an adapter pair** in `predicted_geometry_recovery.py` shaped like
   `_default_context_fusion` / `_default_unsupported_suppression`:
   - `fuse_context(predicted_geometry, channel) -> fused_geometry`
   - `suppress_unsupported(rows, channel) -> rows`
   Pass them and `context_label="<context>"` to
   `build_in_distribution_predicted_geometry_recovery` (or via the CLI
   `--reconstruction-channel` / `--context-label`). Everything else is reused.

6. **Measure** out-of-sample recovery on the calibration split. Iterate the
   channel (more classes, better localization, confidence) until the recovery and
   regression numbers are convincing.

7. **Only then** stage the **heldout one-shot** application and request explicit
   authorization to read it.

## Guardrails (apply to every family)

- Supervise channels with **structural observations only**; never the mechanism
  fingerprint, EC, Rhea, mechanism text, or labels.
- **Heldout is one-shot.** Develop entirely on train/calibration; out-of-sample
  recovery is the calibration split. Do not read heldout until the head +
  threshold are fixed and the read is authorized.
- Report **out-of-sample** recovery as the headline; in-sample (train) is a
  reference only.
- No registry / ontology / production-scorer / global-threshold changes from this
  pipeline.

## Key files

- `src/catalytic_earth/predicted_geometry_robustness.py` — predicted-geometry
  features, failure decomposition, router rows, restoration/graft probes.
- `src/catalytic_earth/cofactor_presence_calibration.py` — reference
  reconstruction channel (leakage-safe).
- `src/catalytic_earth/predicted_geometry_recovery.py` — the family-agnostic
  recovery harness (context adapters: `_default_context_fusion`,
  `_default_unsupported_suppression`).
- `src/catalytic_earth/geometry_retrieval.py` — `score_entry_against_fingerprint`
  (where the router consumes injected context).
