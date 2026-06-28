# Option B: New Held-Out Pre-Registration (repaired fine-57 router)

Run: 2026-06-28T23:18:15Z
Status: `preregistered_not_yet_run_pending_router_fix`

## Why

- The M-CSA held-out is spent (~14 rows left, 1 in-scope), so a repaired fine-57 router cannot be validated on a fresh M-CSA held-out. This freezes the next best untouched validation vehicle before any router fix.

## Primary Hypothesis

- A repaired fine-57 router that constrains the metal v2-subclasses will, on this never-seen set, (a) recover true mechanism families at >= the bar AND (b) stop routing non-metal (flavin/heme/PLP) positives into metal subclasses (the Gate-1 failure mode).

## Frozen Held-Out Set

- Untouched high-confidence, atlas-family, non-M-CSA bronze positives, disjoint from train/cal, M-CSA accessions, and the off-M-CSA recovery development set. Enumerated and content-hashed.
- Counts: 22 total (13 non-metal, 9 metal).
- Content hash (sha256): `7ffa38d8505d90f9354d7455d21516831871586ae17b56a5236670ea3d8b1d68`.

## Pre-Committed Pass Bar

- Min recovery rate: 0.7.
- Max non-metal-into-metal misroute rate: 0.2.
- Derivation: Recovery floor mirrors the held-out one-shot bar (0.70). The non-metal misroute ceiling (0.20) targets the Gate-1 failure mode directly: on M-CSA calibration 7/8 misroutes were non-metal enzymes routed into metal subclasses; a repaired router should keep that well under 1-in-5 on never-seen non-metal positives. Both fixed before any held-out scoring.

## Execution Procedure (after the router fix, one shot)

1. Repair the fine-57 router on TRAIN/CAL only (constrain the metal v2-subclasses so they require metal-cofactor support; re-verify calibration recovery moves toward 30/35).
2. Freeze the repaired-router rule (its own pre-registration / sha) BEFORE touching this held-out.
3. Materialise AlphaFold structures for the frozen held-out accessions (bounded download; verify the sha256 first).
4. Score the held-out once through the repaired router; compute recovery rate and non-metal-into-metal misroute rate.
5. Compare to PASS_BAR; emit PASS/FAIL verbatim and stop. Run once.

## Caveats

- Small n (22 positives; 13 non-metal, 9 metal) -- a focused failure-mode probe, not a high-precision estimate.
- Bronze labels are automation-curated (concordance, not gold truth).
- Off-M-CSA and structure-materialisation-gated; a deployment-grade validation would need gold-curated rows.

## One-Shot Guardrail

- Run exactly once, after the repaired-router rule is frozen. No post-hoc change to the rule, bar, or set; any re-run invalidates this pre-registration.

## Guardrails

- No held-out row scored; set is untouched by development; pass bar fixed from first principles before scoring; no registry/ontology/label change.
