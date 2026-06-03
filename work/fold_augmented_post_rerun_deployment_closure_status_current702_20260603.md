# Fold-Augmented Post-Rerun Deployment Closure Status - current702

Run: 2026-06-03T00:57:46Z

Deployment-closure status after the fixed-threshold Lever 3 combined rerun readout and calibration-impact audit. This composes prior confounded-readiness metrics with the new train/cal blocker status; it does not rerun scores, tune thresholds, or inspect heldout rows.

## Status

- fold_augmented_post_rerun_deployment_closure_status_blocked_p10746_caveat
- Fixed threshold: 0.44155
- Prior remaining production blocker rows: 5
- Remaining combined-score blocker rows: 1
- Expanded full-channel score rows: 75/76
- Heldout confounded OOS abstained: 5/6

## Blocker Disposition

| row | status | combined | abstains |
| --- | --- | ---: | --- |
| m_csa:78 | fixed_threshold_combined_readout | 0.4054 | True |
| m_csa:531 | fixed_threshold_combined_readout | 0.4756 | False |
| uniprot:P78549 | fixed_threshold_combined_readout | 0.42485 | True |
| uniprot:Q3LXA3 | fixed_threshold_combined_readout | 0.4483 | False |
| m_csa:204 | fold_only_policy_caveat_not_combined_scored | None | None |

## Decision

- Deployable without production caveat: False
- Resolve the P10746 fold-only caveat or explicitly accept it as a deployment caveat; no additional mechanical combined-score blockers remain after the fixed-threshold rerun.
