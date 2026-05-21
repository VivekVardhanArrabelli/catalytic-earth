# ePK false-positive hunter handoff

- Last updated: 2026-05-21T05:22:42Z
- Started: 2026-05-21T04:32:59Z
- Ended: 2026-05-21T05:22:42Z
- Measured minutes: 49.72
- Primary outcome: regression_rows_emitted
- Pushed commit: 1a712f04adc071a2faafb917bd0735409f17e092 via alternate-index commit/push.
- Handoff/status commit: aca2612f65489584bcaa982a93671ed4d36ef0df via alternate-index commit/push.
- Rule under attack: entry-level any-context v4 review-only guard overblock risk plus unsafe ePK materializer non-abstention on geometry-prefiltered non-ePK v4 contaminants.
- Production claim allowed: false
- Labels/fingerprints changed: false

## Search Surface

Ran a new lane-only helper over source-valid ePK entity seeds and geometry-prefiltered non-ePK v4 contaminants. CIFs were fetched in memory only and reduced to compact context/materializer evidence.

- Helper: `tools/research_lanes/epk_false_positive_hunter/source_valid_epk_seed_geometry_prefilter_stress.py`
- Primary artifact: `artifacts/research_lanes/epk_false_positive_hunter/source_valid_epk_seed_geometry_prefilter_stress_20260521_043259Z.json`
- Extended gate: `artifacts/research_lanes/epk_false_positive_hunter/epk_candidate_evidence_v1_regression_gate_20260521_051511Z.json`
- V4 absence audit: `artifacts/research_lanes/epk_false_positive_hunter/source_valid_epk_seed_v4_absence_audit_20260521_051700Z.json`
- Entries reviewed: 404
- Coordinate contexts reviewed: 904
- Materializer contexts: 39
- Source-valid family-bucket entries: 27
- Source-valid deposited-or-assembly v4 seeds: 1, `9LGO`
- Non-ePK v4 contaminant prefilter entries: 67
- Local gamma-to-acceptor geometry contexts: 145
- Geometry-prefiltered non-ePK materialized contexts: 8
- Fetch errors: 0
- Materializer context errors: 0

## Result

No new unsafe ePK non-abstention was found on this bounded surface.

- `9LGO` was the only polymer/entity-classified source-valid ePK seed with deposited-or-assembly v4 true. Deposited and biological assembly contexts both returned zero substrate-mode materializer hits.
- `8OOZ`, `9OFD`, `9OFE`, and `9W1G` had local gamma-to-acceptor geometry in deposited and biological assembly contexts, but all eight materializer probes returned `no_heteromeric_candidate_hit_review_only`.
- The extended `epk_candidate_evidence_v1` regression gate emitted 305 rows, including 10 rows from the new source artifact: 8 geometry-prefiltered non-ePK contaminant controls and 2 source-valid ePK entity-seed controls.
- Expected-policy unsafe non-abstentions remained 0.
- The pinned context-v4-only assembly split failure remains `5UJ7:biological_assembly_1`.

## Evidence For / Against

Evidence for the regression gate extension:

- The new helper preserves coordinate context, local geometry, deposited/assembly v4 state, entry-level guard state, regression-gate join state, expected source/policy category, and observed materializer decision.
- The gate now covers a sharper contaminant surface than the previous no-hit pass because non-ePK entries were prefiltered for local Tyr or N-terminal Ser/Thr/Tyr gamma geometry before materialization.

Evidence against counterexamples on this run's surface:

- No source-valid ePK overblock was observed because the only entity-classified v4 source seed, `9LGO`, produced no substrate-mode materializer hit.
- No geometry-prefiltered non-ePK residual survived materialization; all eight selected contaminant contexts abstained.
- Of 27 source-valid family-bucket entries, 26 lacked deposited-or-assembly v4 and were outside the entry-level v4 overblock surface.

## Verification

- `python -m py_compile tools/research_lanes/epk_false_positive_hunter/source_valid_epk_seed_geometry_prefilter_stress.py tools/research_lanes/epk_false_positive_hunter/epk_candidate_evidence_regression_gate.py`
- `python -m json.tool artifacts/research_lanes/epk_false_positive_hunter/source_valid_epk_seed_geometry_prefilter_stress_20260521_043259Z.json >/dev/null`
- `python -m json.tool artifacts/research_lanes/epk_false_positive_hunter/epk_candidate_evidence_v1_regression_gate_20260521_051511Z.json >/dev/null`
- `python -m json.tool artifacts/research_lanes/epk_false_positive_hunter/source_valid_epk_seed_v4_absence_audit_20260521_051700Z.json >/dev/null`
- `git diff --check -- tools/research_lanes/epk_false_positive_hunter/source_valid_epk_seed_geometry_prefilter_stress.py tools/research_lanes/epk_false_positive_hunter/epk_candidate_evidence_regression_gate.py artifacts/research_lanes/epk_false_positive_hunter/source_valid_epk_seed_geometry_prefilter_stress_20260521_043259Z.json artifacts/research_lanes/epk_false_positive_hunter/epk_candidate_evidence_v1_regression_gate_20260521_051511Z.json artifacts/research_lanes/epk_false_positive_hunter/source_valid_epk_seed_v4_absence_audit_20260521_051700Z.json`

## Blockers

- `git fetch origin` failed writing linked-worktree `FETCH_HEAD`: Operation not permitted.
- `git pull --ff-only origin research/epk-false-positive-hunter` failed writing linked-worktree `FETCH_HEAD`: Operation not permitted.
- `git fetch --no-write-fetch-head origin` succeeded.
- Normal `git add` failed creating linked-worktree `index.lock`: Operation not permitted.
- Alternate-index primary commit/push succeeded.
- Alternate-index handoff/status commit/push succeeded.
- Local checked-out HEAD remains behind `origin/research/epk-false-positive-hunter`; normal status still reflects linked-worktree metadata/index issues from prior runs.

## Next Query

Audit the materializer-equivalence gap for local geometry prefilter rows `8OOZ`, `9OFD`, `9OFE`, and `9W1G`: compare local gamma-to-acceptor geometry with heteromeric entity mapping to explain why the actual materializer abstains, then expand later-offset CDK/cyclin, mTORC1/2, JNK, and receptor tyrosine kinase entity seeds to look for deposited-or-assembly v4 positives beyond `9LGO`. Keep production labels, thresholds, registries/fingerprints, migrations, and scoring forbidden.

Production claims, label changes, threshold calibration, registry/fingerprint edits, artifact migrations, and production scoring remain forbidden.

## Files Changed

- `tools/research_lanes/epk_false_positive_hunter/source_valid_epk_seed_geometry_prefilter_stress.py`
- `tools/research_lanes/epk_false_positive_hunter/epk_candidate_evidence_regression_gate.py`
- `artifacts/research_lanes/epk_false_positive_hunter/source_valid_epk_seed_geometry_prefilter_stress_20260521_043259Z.json`
- `artifacts/research_lanes/epk_false_positive_hunter/epk_candidate_evidence_v1_regression_gate_20260521_051511Z.json`
- `artifacts/research_lanes/epk_false_positive_hunter/source_valid_epk_seed_v4_absence_audit_20260521_051700Z.json`
- `artifacts/research_lanes/epk_false_positive_hunter/epk_false_positive_hunter_runs.jsonl`
- `work/research_lanes/epk_false_positive_hunter/handoff.md`
