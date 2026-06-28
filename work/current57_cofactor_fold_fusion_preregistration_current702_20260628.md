# Current-57 Cofactor + Fold-NN Fusion Preregistration

Run: 2026-06-28T12:06:11Z
Status: `blocked_current57_cofactor_fold_fusion_not_deployable`

## Rule

- retained_in_scope_call := fused.top1_score >= cofactor_threshold AND fold_nn_alntmscore >= fold_threshold; correctness uses the documented legacy-v1 metal-umbrella compatibility projection.
- Fold channel role: out_of_scope_rejection_abstention_gate.

## Done Bar (trusted June 9, calibration)

- Required recovery: >= 30/35.
- OOS FP ceiling: <= 8/26.

## Recovery Ceiling (current-57 router)

- Compatible recovery ceiling: 26/35.
- Exact recovery ceiling: 13/35.

## Fold-NN Marginal Value

- Cofactor-only best under OOS-FP ceiling: cofactor 0.7388 + fold 0.0: recall 20/35 (0.5714) · OOS FP 6/26 (0.2308).
- Fusion best under OOS-FP ceiling: cofactor 0.5539 + fold 0.4761: recall 23/35 (0.6571) · OOS FP 8/26 (0.3077).
- Fold recovery gain at the OOS-FP ceiling: 3.
- Max-precision point (>= cofactor-only recovery): cofactor 0.5539 + fold 0.615: recall 20/35 (0.5714) · OOS FP 5/26 (0.1923).

## Eligibility

- Eligible calibration points clearing the done bar: 0.
- Decision: `fail_closed_keep_atlas_engine_blocked_on_current57_cofactor_surface`.

## Deployment Decision

- Fail closed for atlas-engine fusion on the current-57 cofactor surface. The binding constraint is the current-57 router's compatible-recovery ceiling, not OOS false positives, so the documented next step is to pin/replay the intended June 9 router/fingerprint surface (whose recovery clears the bar) and then re-apply this fold-NN OOS-rejection gate. The high-precision fusion regime (near-zero OOS FP at reduced recovery) is a separate, narrower product framing that would still require heldout confirmation.

## Guardrails

- Fold scores are calibration-vs-train only; no heldout row was scored or read.
- No threshold was selected on heldout rows; no supervised model was trained.
- No production threshold, model weight, registry, ontology, label, or fingerprint-family change was made.
