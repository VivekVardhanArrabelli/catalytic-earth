# Predicted-Atlas Versus Fold Novelty Operating-Grid Delta - current702

Run: 2026-06-01T23:16:25Z

Review-only delta audit comparing frozen predicted-atlas geometry novelty operating-grid rows against frozen geometry-plus-predicted-fold operating-grid rows. It reads existing artifacts only and does not select a deployment threshold.

## Status

- predicted_atlas_vs_fold_novelty_delta_ready_review_only
- Shared retention targets: 4
- Targets with OOS abstain lift: 4
- Targets with confounded abstain lift: 4
- Critical violations: 0

## Delta Rows

| target | geometry OOS | fold OOS | OOS delta | geometry confounded | fold confounded | confounded delta |
| ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| 0.80 | 0.6203 | 0.8608 | 0.2405 | 0.6667 | 0.8333 | 0.1666 |
| 0.85 | 0.5949 | 0.8354 | 0.2405 | 0.6667 | 0.8333 | 0.1666 |
| 0.90 | 0.2278 | 0.7722 | 0.5444 | 0.3333 | 0.8333 | 0.5 |
| 0.95 | 0.1519 | 0.6456 | 0.4937 | 0.1667 | 0.8333 | 0.6666 |

## Interpretation

- Fold-augmented novelty materially improves the frozen predicted-atlas operating-grid diagnostic at matched retention.
- Use the fold-augmented train/cal threshold contract for any thresholded claim; keep this heldout operating-grid comparison review-only.
