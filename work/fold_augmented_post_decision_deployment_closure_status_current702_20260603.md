# Fold-Augmented Post-Decision Deployment Closure Status - current702

Run: 2026-06-03T10:19:58Z

Post-decision Lever 3 deployment closure status. It composes the post-rerun confounded closure audit with the P10746 decision application gate. It closes only if the P10746 fold-only caveat is explicitly accepted and the existing operating-point criteria remain met.

## Status

- fold_augmented_post_decision_deployment_closure_blocked_pending_p10746_decision
- Heldout confounded OOS abstained: 5/6
- Expanded full-channel rows: 75/76
- Remaining combined-score blockers: 1
- P10746 caveat accepted rows: 0
- P10746 pending decision rows: 1
- Blockers: p10746_fold_only_caveat_not_accepted

## Decision

- Deployment closed with P10746 caveat: False
- Next gate: Apply an explicit P10746 accept decision with unchanged context hash, then rerun this closure status. If the caveat is rejected, provide an approved non-residue sidecar before closure.

## Interpretation

- The fold channel remains research-ready at the operating point, but deployment closure is blocked until the P10746 fold-only caveat is explicitly accepted or replaced by an approved non-residue sidecar.
- Review/apply the P10746 decision stub, then regenerate this post-decision closure status.
