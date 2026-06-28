# Held-Out One-Shot Pre-Registration

Run: 2026-06-28T17:16:16Z
Status: `preregistered_not_yet_run`

## Why

- All session operating points are calibration development figures (the calibration rows were inspected repeatedly), so they are optimistic and unvalidated. This locks the single unbiased test before it is run so the result cannot be cherry-picked.

## Primary Hypothesis

- The June 9 router at the 0.44 cofactor dial (calibration 30/35 recovery, 8/26 OOS FP) generalizes to the never-seen held-out M-CSA split at the pre-committed bar.

## Frozen Rule

- Router: cofactor_fusion_operating_point builder with the fingerprint registry pinned to git commit d567ee0d (the June 9 state: 8 fingerprint families), default graph artifacts/v1_graph_1025.json, label manifest v3_sequence_nn_label_manifest_current702_20260525, channel v3_cofactor_presence_calibration_current702_20260604, alphafold_version 6
- Cofactor threshold: 0.44; fold gate: off.
- In-scope correct: fused.top1_fingerprint_id == frozen true_fingerprint_id AND fused.top1_score >= 0.44 (identical to the builder's fused_correct_at_threshold that produced the calibration 30/35).
- OOS false positive: fused.top1_score >= 0.44 on an OOS row.

## Pre-Committed Success Bar

- Calibration reference: recovery 30/35 (0.857), OOS FP 8/26 (0.308).
- PASS criteria: heldout in-scope recovery rate >= 0.70 AND heldout OOS false-positive rate <= 0.40.
- Derivation: Calibration recovery 0.857 has SE ~0.059 on n=35, so ~2 SE below is ~0.74; rounded conservatively to a 0.70 floor. Calibration OOS-FP 0.308 has SE ~0.090 on n=26, so ~2 SE above is ~0.49; rounded conservatively to a 0.40 ceiling. Both bars were fixed before any held-out row was scored.

## Frozen Held-Out Set

- current702 label rows not in the train/cal split manifest that also have a staged held-out structure (scoreable). Enumerated and content-hashed so the evaluated set cannot be swapped or trimmed after the fact.
- Counts: 126 total (47 in-scope, 79 OOS).
- Content hash (sha256): `45632519a2b2f9645c2bb82a9fbff681dde34cfda21dde720550402c0bb907b6`.

## Execution Procedure (authorized one-shot)

1. In an isolated git worktree at HEAD, pin the registry: git checkout d567ee0d -- data/registries/mechanism_fingerprints.json data/registries/mechanism_ontology.json (the main repo registry is never mutated).
2. Construct a held-out split manifest containing exactly the 126 frozen_heldout_set entry_ids (verify sha256 first).
3. Run the cofactor_fusion_operating_point router over the held-out coordinate dirs at cofactor_threshold 0.44, producing fused per-row calls and scores for the frozen held-out rows only.
4. Count in-scope recovery (fused exact match at threshold) and OOS false positives (fused retained at threshold); compute the two rates.
5. Compare to SUCCESS_BAR.primary_pass_criteria; emit PASS or FAIL verbatim and stop. Report the secondary fold-gated point for information only.

## One-Shot Guardrail

- Run exactly once. Report the resulting counts verbatim. Do not adjust the rule, thresholds, correctness definition, or row set after observing any held-out result. Any re-run or post-hoc change invalidates this pre-registration.

## Guardrails

- No held-out row was scored; held-out labels were used only to size and freeze the set, never as features.
- The success bar was derived from calibration only, before any held-out scoring.
- No registry, ontology, label, threshold, or model change.
