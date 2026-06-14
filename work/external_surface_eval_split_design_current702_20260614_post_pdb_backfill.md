# External Surface Eval Split Design - post PDB backfill

Artifact: `artifacts/v3_external_surface_eval_split_design_current702_20260614_post_pdb_backfill.json`

SHA-256: `790a8bd092558d852e6e0ca02fe45557cc14a0eb07217fb0280a58ea6748c38e`

Design only. No benchmark was run, no threshold was selected, and no registry/tier change occurred.

## Current Surface

- External bronze rows: 6862 = 5638 positive bronze + 1224 OOS bronze.
- Combined label surface: 7564; combined seed surface: 5868.
- Rows with PDB IDs: 2020; holo-confirmed rows: 260; silver-ready pending geometry: 260.
- Silver confirmed tier count remains 17; silver flips in this design: 0.

## Design

- Split by entry with sequence-cluster and family-block grouping before assignment.
- Reserve external rows by family, source-time, sequence-cluster novelty, and OOS tier.
- Treat PDB/holo/silver-ready as diagnostics/strata only, never as predictive features.
- Keep positive_bronze, OOS, silver_ready, silver_confirmed, and projected counters separate in all metrics.

## Before Any Benchmark

- Freeze a split manifest with row hashes and sequence-cluster deduplication.
- Freeze OOS tiers and threshold-selection rules before looking at test outcomes.
- Write a feature manifest proving excluded_context fields are not predictive inputs.
- Run leakage/source-contract tests on the exact feature artifact.

Next action: build the frozen external-surface split manifest; do not run a benchmark until leakage and split audits pass.
