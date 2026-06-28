# Session Decision Record — 2026-06-28

Consolidated progress, decisions, and findings for the deployment-line work of
2026-06-28. This is a durable summary; the machine artifacts named below are the
source of truth, and `docs/decision_log.md` holds the dated rulings.

All refs are in sync at the end of the session: `main == origin/main ==
claude/continue-last-commit-ytktge` (the work was merged into `main` via a clean
fast-forward).

---

## 1. Headline outcomes

1. **First validated deployment claim (M-CSA).** The locked, pre-registered
   held-out one-shot was executed once and **PASSED**: the June 9 cofactor-fusion
   router at the 0.44 dial recovers **35/47 (0.745)** in-scope mechanisms at
   **15/79 (0.190)** OOS false-positive rate on the never-touched held-out M-CSA
   split — clearing the pre-committed bar (recovery ≥ 0.70, OOS-FP rate ≤ 0.40).
   This is the project's first leakage-safe, pre-registered, validated
   mechanism-recovery result. Scope: **M-CSA only**.

2. **The fold (structural nearest-neighbour) channel generalises off M-CSA on
   BOTH halves** — recovery and rejection — the property the cofactor channel
   lacked:
   - **Recovery:** fold-NN retrieval against the M-CSA atlas recovers the true
     mechanism for **132/156 (0.846)** off-M-CSA bronze positives, across all 4
     cofactor families (flavin 0.86, metal-hydrolase 0.76, heme-peroxidase 0.85,
     PLP 1.00) — on par with the M-CSA in-distribution baseline (28/35 = 0.80).
   - **Rejection:** external non-M-CSA negatives have fold-NN median **0.574** ≈
     M-CSA OOS **0.566**, far below in-scope **0.743**; a strict gate (fold ≥
     0.70) abstains on 49/52 (94%) of them.
   This is the strongest evidence in the project that the structural-retrieval
   lever is real, not an M-CSA artifact. (Non-circular: bronze admission used
   sequence/cofactor, never structure.)

3. **Gate 1 (router reconciliation) resolved on evidence:** the production
   current-57 fine router's drift from the validated June 9 router is **genuine
   misrouting, not taxonomy relabeling** — so **adopt the June 9 coarse router**
   as the deployable baseline.

---

## 2. The work, in order (what each step found)

| Artifact (`artifacts/…`) | Finding |
|---|---|
| `v3_current57_fold_tm_recompute_readout_current702_20260628` | Recomputed Fold/TM via foldseek; **row alignment resolved** (35/35 in-scope, 26/26 OOS vs cached 4/35, 0/26). In-scope fold-NN median **0.743** vs OOS **0.566**; fold-NN recovers true fingerprint 28/35. |
| `v3_current57_cofactor_fold_fusion_preregistration_…` | Cofactor+fold fusion **fail-closed**: fold gate adds +3 recovery at the OOS-FP ceiling (cofactor-only 20/35 → fusion 23/35 @ FP 8), but the current-57 **compatible-recovery ceiling is 26/35 < the 30/35 bar**. Binding constraint = recovery, not OOS FP. |
| `v3_june9_router_pinned_rowdetail_…`, `v3_june9_router_fold_fusion_readout_…` | Reproduced the June 9 router (registry pin `d567ee0d`) exactly: **30/35 @ 9 FP** frozen, **30/35 @ 8 FP** at the 0.44 dial. On the *healthy* router the fold gate gives **no Pareto improvement** (residual OOS FPs are high-fold-similar; 7/8 are `metal_dependent_hydrolase`) — it's a precision/recall dial there (28/35@6, 23/35@1, 18/35@0). |
| `v3_external_offmcsa_fold_abstention_readout_…` | **Off-M-CSA abstention generalises** (see Headline 2). |
| `v3_offmcsa_recovery_feasibility_…` → `v3_offmcsa_recovery_download_manifest_…` | Off-M-CSA recovery was data-blocked (no locally-structured trusted non-M-CSA positives); resolved by a bounded, signed-off AlphaFold download of 162 trusted bronze positives (~97 MB). |
| `v3_fold_nn_mechanism_recovery_offmcsa_bronze_…` | **Off-M-CSA recovery 132/156 (0.846)** (see Headline 2). |
| `v3_fold_nn_mechanism_recovery_mcsa_baseline_…` | M-CSA in-distribution recovery baseline **28/35 (0.80)**; as a confidence gate it is high-precision (fold ≥ 0.65 → **24/25 = 0.96** precision at 0.69 recovery). |
| `v3_heldout_oneshot_preregistration_…` | **Locked** the one-shot: frozen rule (June 9 router @ 0.44), frozen 126-row set (sha `45632519…`), pre-committed bar — all before any held-out read. |
| `v3_fold_channel_deployment_readiness_summary_…` | Verifiable aggregate of the above (reads source values + sha256). |
| `v3_atlas_broadening_feasibility_…` | Broadening beyond the 5 cofactor families is **data-blocked**: fine 57-family M-CSA truth labels exist only on the cofactor surface (52/57 families unreachable). |
| `v3_heldout_oneshot_eval_result_…` | **DEPLOYMENT CLAIM** — held-out one-shot **PASS** (see Headline 1). |
| `v3_router_reconciliation_diagnostic_…` | **Gate 1** — fine-57 drift is genuine misrouting (see §3). |
| `v3_option_b_heldout_preregistration_…` | **Option B** new held-out frozen; M-CSA held-out exhausted (see §4). |

---

## 3. Gate 1 — router reconciliation (decision: adopt June 9 coarse router)

On the 35 calibration in-scope rows (threshold 0.4115): the current-57 fine
router is **exact 13/35**; documented v2-split relabeling lifts it only to
**26/35**, still **4 short** of the June 9 reference **30/35**. It is **not
reconcilable by relabeling** — **8 rows are genuine misroutes**, and **7 are
non-metal (flavin/heme/PLP) enzymes over-claimed by the fine-57 metal v2-subclass
fingerprints** in the fused geometry router. The coarse June 9 router has no
metal subclasses and so does not misroute them (hence 30/35).

- **Option A — adopt the June 9 coarse router (RECOMMENDED):** the deployable,
  held-out-validated baseline now; coarse (~8-family) granularity; zero further
  work.
- **Option B — repair the fine-57 router:** a real router fix with an identified
  root cause (metal-subclass over-claiming), requiring a NEW pre-registration
  against a NEW held-out. Pursue only if production needs fine metal-subclass
  calls.

---

## 4. Option B — started; the held-out is the blocker

Pursued Option B the leakage-safe way (freeze the validation vehicle before any
fix) and found a hard fact: **the M-CSA held-out is exhausted.** Of the 140-row
designated partition, the deployment one-shot spent 126; only **14 remain
untouched (1 in-scope, 13 OOS), none with structures**. So a repaired fine-57
router cannot be validated on a fresh M-CSA held-out.

A new held-out was frozen from untouched off-M-CSA bronze
(`v3_option_b_heldout_preregistration_…`): **22** high-confidence atlas-family
non-M-CSA positives (**13 non-metal, 9 metal**; the split directly probes the
Gate-1 failure mode), disjoint from train/cal, M-CSA, and the recovery
development set, content-hashed `7ffa38d8…`. Pre-committed bar: recovery ≥ 0.70
AND non-metal→metal misroute ≤ 0.20.

Remaining Option-B steps (NOT done): (1) repair the fine-57 router on train/cal
(constrain metal v2-subclasses to require metal-cofactor support); (2) freeze the
repaired-router rule; (3) materialise structures for the 22 and spend the
held-out once.

---

## 5. Decisions made

1. **Adopt the June 9 coarse router** as the deployable, validated baseline
   (Gate 1, Option A recommended over Option B).
2. **Spent the held-out one-shot** under its frozen rule — it is now used and
   must not be re-run.
3. **Did not spend held-out on low-information confirmations** — declined to burn
   it on M-CSA-only checks earlier; pivoted to off-M-CSA tests, which carry the
   deployment-relevant signal.
4. **Merged the session into `main`** as a clean fast-forward (see §7).
5. **Did not grow fingerprint families** and **did not mutate any registry** all
   session (verified: 0 files under `data/` changed; frozen gold core
   `curated_mechanism_labels.json` = `94f98ebe` unchanged).

---

## 6. Honest limitations (what is NOT yet validated)

- The validated held-out claim certifies **M-CSA only**; a SwissProt-wide claim
  is not established.
- Off-M-CSA recovery uses **bronze** (automation-curated) labels — it measures
  fold/sequence **concordance**, not gold accuracy.
- All calibration operating points are **development figures** (the calibration
  rows were inspected repeatedly); only the held-out read is unbiased.
- Atlas coverage is the **5 cofactor families** only.
- The Option-B held-out is **small (n=22)** and bronze — a focused failure-mode
  probe, not a precise estimate.

---

## 7. Repository / data integrity note (a correction for the record)

Mid-session I incorrectly claimed `main` and the working branch had "unrelated
histories with divergent registries." That was a **shallow-clone artifact** —
`git rev-parse --is-shallow-repository` was true and `.git/shallow` held the
apparent "roots". After `git fetch --unshallow`, the real common ancestor is
`79dc2d3a` (the session base), the shared root is `93806418 Initialize Catalytic
Earth scaffold`, and the branch was always a **strict superset** of `main` (148
ahead, 0 behind). The merge was a clean fast-forward.

A full registry audit confirmed **nothing under `data/` was altered, lost, or
corrupted**: all four registries at HEAD are byte-identical to the session base
(`mechanism_fingerprints` `19d837f1`, `mechanism_ontology` `39c68c1b`,
`curated_mechanism_labels` `94f98ebe`, `external_bronze_labels` index
`1d91dc20`); the 5 bronze shards verify against their index (9,299 rows);
`validate` returns 57 fingerprints / 54 families / 702 labels. Lesson recorded:
check for a shallow clone before ever concluding "unrelated histories".

---

## 8. Forward roadmap (next phase)

Destination: a **gold-validated, structurally-gated mechanism atlas** that makes
abstaining mechanism calls on the deployment distribution, served by one
reconciled router.

- **Gate 1 — router reconciliation: DONE.** Adopt the June 9 coarse router.
- **Gate 2 — gold off-M-CSA validation:** curate a small gold (not bronze)
  non-M-CSA positive set + structures; run the existing recovery harness. The
  single highest-credibility-per-effort step beyond M-CSA.
- **Gate 3 — productionise the fold channel:** sequence → AlphaFold structure →
  fold-NN vs atlas → mechanism call + confidence + abstain-below-threshold; pick
  the operating point on the measured precision/recovery curve.
- **Gate 4 — broaden coverage (blocked):** derive fine multi-family M-CSA truth
  labels + structures to grow the atlas past the cofactor families.
- **Option B (optional):** finish the fine-57 router repair and spend the frozen
  bronze held-out (`7ffa38d8…`).

Discipline carried forward: the M-CSA held-out is spent, so every future
operating-point change needs a NEW pre-registration against a NEW held-out
(ideally including non-M-CSA gold rows). Do not re-run the spent one-shot; do not
grow fingerprint families.
