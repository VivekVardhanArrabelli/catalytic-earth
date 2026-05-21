# ePK false-positive hunter handoff

- Last updated: 2026-05-21T14:17:26Z
- Started: 2026-05-21T13:21:25Z
- Ended: 2026-05-21T14:17:26Z
- Measured minutes: 56.02
- Primary outcome: regression_rows_emitted
- Pushed evidence commit: 5dc15ecc9e62fa18bcd680fd4815420329ebf625 via alternate-index commit/push.
- Rule under attack: later-offset source-valid ePK entity/title seed coverage plus materializer equivalence on local geometry prefilters; regression gate for ATPase/transporter/ORC-MCM/motor/same-chain/internal-fragment/ligand-materialization controls.
- Production claim allowed: false
- Labels/fingerprints changed: false

## Search Surface

Ran the expanded later-offset retry requested by the previous handoff, with broader CDK/cyclin, JNK, RTK/EGFR, insulin receptor, and mTORC1/2 query terms plus lane-only entity/title fallback buckets. CIFs were fetched in memory and reduced to compact summaries; no raw coordinate dumps were written.

- Expanded helper artifact: `artifacts/research_lanes/epk_false_positive_hunter/source_valid_later_offset_gap_audit_expanded_20260521_132125Z.json`
- Refreshed regression gate: `artifacts/research_lanes/epk_false_positive_hunter/epk_candidate_evidence_v1_regression_gate_20260521_141548Z.json`
- Helpers: `tools/research_lanes/epk_false_positive_hunter/source_valid_later_offset_gap_audit.py`, `tools/research_lanes/epk_false_positive_hunter/epk_candidate_evidence_regression_gate.py`
- Reviewed 523 unique PDB IDs, 522 entry rows, and 1,153 coordinate contexts.
- Materialized 18 selected contexts: eight fixed local-geometry gap controls plus ten source-valid later-offset seed contexts.
- Fetch errors: one transient `1Y64` connection reset.
- Materializer context errors: zero.
- Raw coordinate files written: false.

## Result

No new unsafe ePK non-abstention was found on this expanded bounded surface.

- Source-valid later-offset v4 seed entries were `3GT8`, `4UX9`, and `9LGO`.
- `3GT8` entered through the new EGFR/RTK title fallback and contributed three deposited/assembly overblock-control rows; all returned `no_substrate_mode_materializer_hit`.
- `4UX9` remained the JNK seed and contributed five deposited/assembly control rows; all returned `no_substrate_mode_materializer_hit`.
- `9LGO` remained the CDK/cyclin-family seed and contributed two deposited/assembly control rows; both returned `no_substrate_mode_materializer_hit`.
- The 8OOZ/9OFD/9OFE/9W1G geometry-gap controls again abstained and were explained by same-chain/same-entity materializer mapping.
- The refreshed gate emitted 323 `epk_candidate_evidence_v1` rows. `unsafe_nonabstention_after_expected_policy_count` stayed 0.
- The pinned `5UJ7:biological_assembly_1` context-v4-only biological-assembly split failure remains present and keeps context-v4-only sufficiency falsified.

## Evidence For / Against

Evidence for the regression gate extension:

- Added five additional `source_valid_later_offset_epk_seed_overblock_control` rows beyond the previous 318-row gate, bringing that control class to ten rows.
- Preserved `3GT8` as a title-fallback EGFR/RTK source-valid v4 seed with deposited and biological-assembly contexts.
- Preserved coordinate state, guard hit/miss, expected/observed materializer decision, and candidate fields in the gate rows.

Evidence against counterexamples on this run's surface:

- No source-valid later-offset seed context produced a substrate-mode materializer hit.
- No local geometry gap context had a heteromeric-entity-eligible materializer-equivalent hit.
- No materializer context errors occurred across the selected 18 contexts.
- Expected-policy unsafe non-abstentions remained zero across 323 regression rows.

## Verification

- `python -m py_compile tools/research_lanes/epk_false_positive_hunter/source_valid_later_offset_gap_audit.py tools/research_lanes/epk_false_positive_hunter/epk_candidate_evidence_regression_gate.py`
- `python -m json.tool artifacts/research_lanes/epk_false_positive_hunter/source_valid_later_offset_gap_audit_expanded_20260521_132125Z.json >/dev/null`
- `python -m json.tool artifacts/research_lanes/epk_false_positive_hunter/epk_candidate_evidence_v1_regression_gate_20260521_141548Z.json >/dev/null`
- `git diff --check -- tools/research_lanes/epk_false_positive_hunter/source_valid_later_offset_gap_audit.py tools/research_lanes/epk_false_positive_hunter/epk_candidate_evidence_regression_gate.py artifacts/research_lanes/epk_false_positive_hunter/source_valid_later_offset_gap_audit_expanded_20260521_132125Z.json artifacts/research_lanes/epk_false_positive_hunter/epk_candidate_evidence_v1_regression_gate_20260521_141548Z.json`

## Blockers

- `git fetch origin` failed writing linked-worktree `FETCH_HEAD`: Operation not permitted.
- `git pull --ff-only origin research/epk-false-positive-hunter` failed writing linked-worktree `FETCH_HEAD`: Operation not permitted.
- `git fetch --no-write-fetch-head origin` succeeded.
- Normal linked-worktree index operations remain unreliable because `.git/worktrees/catalytic-earth-epk-false-positive/index.lock` cannot be created.
- Alternate-index commit/push succeeded for the evidence commit.
- Local checked-out HEAD remains behind origin because linked-worktree metadata writes are denied.

## Next Query

Retry the single expanded-surface fetch error `1Y64`, then generalize deposited-v4 / biological-assembly-below-floor split traps outside the fixed ORC/OCCM/MCM panel: search non-ORC AAA+/ATPase/transporter/motor entries where deposited atom_site is v4-positive, a declared biological assembly falls below the current chain floor, and compact Tyr or N-terminal Ser/Thr/Tyr local geometry is heteromeric-entity eligible before materialization. Keep production labels, thresholds, registries/fingerprints, migrations, and scoring forbidden.

Production claims, label changes, threshold calibration, registry/fingerprint edits, artifact migrations, and production scoring remain forbidden.

## Files Changed

- `tools/research_lanes/epk_false_positive_hunter/source_valid_later_offset_gap_audit.py`
- `tools/research_lanes/epk_false_positive_hunter/epk_candidate_evidence_regression_gate.py`
- `artifacts/research_lanes/epk_false_positive_hunter/source_valid_later_offset_gap_audit_expanded_20260521_132125Z.json`
- `artifacts/research_lanes/epk_false_positive_hunter/epk_candidate_evidence_v1_regression_gate_20260521_141548Z.json`
- `artifacts/research_lanes/epk_false_positive_hunter/epk_false_positive_hunter_runs.jsonl`
- `work/research_lanes/epk_false_positive_hunter/handoff.md`
