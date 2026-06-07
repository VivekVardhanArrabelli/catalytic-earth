# Catalytic Earth Session Decision Record — 2026-06-06

Companion to `session_decision_record_20260530.md`. This session built and **confirmed**
the predicted-geometry recovery, added the complementary electron-flow precision lever,
and **consolidated every research branch into `main`**. All numbers below are traceable to
`docs/decision_log.md` entries and the artifacts named here. No labels, registries,
ontologies, production scorers, or global thresholds were changed.

## Session Arc

Pick up from the 2026-05-29 finding (clean experimental 45/45 is not deployable; predicted
apo geometry drops the router to 23/45). Build the leakage-safe sequence -> cofactor channel,
prove it on an in-distribution out-of-sample surface, spend the heldout one-shot to confirm,
then unify all branches and bring the docs current. The throughline: **reconstruct the
deploy-missing active-site context from sequence, and abstain when you can't** — validated
end-to-end on the cofactor instance.

## D1: Reconstruct the cofactor from sequence as a router feature (leakage-safe)

Built `src/catalytic_earth/cofactor_presence_calibration.py`: one-vs-rest metal/flavin/PLP/
heme heads, **fit on the train split, thresholds + backend selected on calibration, heldout
never read for fit/threshold**, supervised only by structural ligand context (never
fingerprint/EC/Rhea/mechanism text). Drop-in compatible with the router's `ligand_context`
injection (the router consumes it via the 0.18-weight `cofactor_context_score`). Artifact:
`v3_cofactor_presence_calibration_current702_20260604.json` (+ a `_motif_` variant adding
leakage-safe cofactor-binding sequence motifs; it lifts head AUC, esp. heme 0.88->0.93, but
did not change the in-distribution recovery count).

## D2: Prove it on an in-distribution out-of-sample surface before spending heldout

Built `src/catalytic_earth/predicted_geometry_recovery.py`: scores the router three ways per
in-distribution row — experimental vs predicted-apo vs cofactor-fused — against the 8
fingerprint templates (no per-row self-match), so the deltas isolate the apo cost and the
recovery. **Honest readout on the calibration split (out-of-sample for the channel):**
experimental 34/35 -> predicted-apo 17/35 -> cofactor-fused **30/35**, recovering **12/17**
apo-lost primaries (70.6%) with 0 regressions. Generalized to any reconstruction context via
injectable adapters + `docs/predicted_geometry_robustness_pipeline_runbook.md`.

## D3: Spend the heldout one-shot — 23 -> 37/45 confirmed; do not tune against it

Authorized single blind pass, frozen channel + threshold 0.4115, nothing refit. Baseline
reproduced 23/45 exactly; cofactor fusion reached **37/45 primary (+14)** — recovering 14 of
the 22 apo-lost (63.6%, matching the out-of-sample 70.6% projection) — at a **precision cost:
OOS/sec FP 12.3% -> 25.9%**. **The one-shot is SPENT; no threshold/policy may be tuned against
it.** Artifact: `v3_heldout_oneshot_cofactor_fusion_blind_pass_current702_20260604.json`.
Foundation (now in main via the youthful Problem-2 merge): decomposition (cofactor-loss-
dominated, 22/22), restoration probe 22/22, graft fidelity 19/22, ESMFold2 apo backend.

## D4: Electron-flow is the complementary precision lever — keep it (corrected mis-archive)

Lever-2's electron-flow track was first mis-archived as a dead-end; on review it had real,
recent (2026-06-06), leakage-safe progress and was merged. A source-free electron-flow OR
overlay raises OOS abstain-recall **0.467 -> 0.507 (+0.04) at primary retention 1.0** (PQQ
`m_csa:104`, NAD-family `m_csa:464`, Fe-S `m_csa:119`); research-grade, pending a protected-
import authorization. It is the **complement** to D3: cofactor adds primary recall (at a
precision cost), electron-flow adds OOS abstention without costing primaries.
(`src/catalytic_earth/lever2_mechanism_incremental_readout.py`,
`v3_lever2_source_free_electron_flow_current_split_operating_point_readout_current702_20260606.json`.)

## D5: Unify all branches into `main`; archive ePK as NO-GO

All research tracks consolidated (PRs #4 cofactor, #5 youthful, #6 lever-2 + trailing
commits; earlier representation-shootout / LOMO-snapshot / organic-cofactor / Lever-2 PRs
already in main). The 5 ePK tracks are **NO-GO** for heuristic geometry and archived as
recoverable tags `archive/epk-*` (conclusions captured; code stays out of main). Verified
exhaustively: only `main` is a live remote branch; every other ref/worktree HEAD is an
ancestor of main; nothing lost.

## D6: The LOMO<->expansion collision must be reconciled BEFORE expansion

LOMO (Leave-One-Mechanism-Out) open-set eval is the generalization yardstick; current LOMO
did not show exact open-set recovery. **Hard constraint:** LOMO needs a frozen pre-expansion
snapshot while expansion adds rows — opposite split semantics. The family-expansion pipeline
must run LOMO against a snapshot tagged before any expansion write and keep expansion row-adds
out of the LOMO split. (See `project_state.md` "Expansion And Generalization Constraints".)

## State At Session End

- Predicted-apo primary: **37/45** (confirmed, one-shot spent), OOS/sec FP 25.9%.
- Live deployable signals: geometry router (45/45 experimental), fold/TM channel (AUC 0.81/0.91),
  cofactor-presence channel (recall), electron-flow (OOS precision, research-grade).
- `main` is the single source of truth; 6 `archive/*` recoverable tags; docs current.
- Open question: the **precision operating point** (suppression vs recalibrated threshold +
  electron-flow), decided on a leakage-safe OOS surface.
- Next build (planned, separate approval): **family-onboarding pipeline** — a thin orchestrator
  that assembles the existing parts (sourcing, channels, splits, robustness, gates) into one
  per-family status manifest, accounting for the LOMO<->expansion collision.

## Non-Negotiables (carried forward)

- Heldout is one-shot and now SPENT for the cofactor channel — do not re-run or tune against it.
- Supervise reconstruction channels with structural observations only; never the mechanism
  fingerprint, EC, Rhea, mechanism text, or labels.
- Report out-of-sample (calibration) recovery as the headline; train is in-sample reference only.
- No registry/ontology/threshold/production-scorer/label changes without the explicit gates.
- Reconcile LOMO before expansion.
