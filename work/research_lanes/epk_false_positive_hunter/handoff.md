# ePK false-positive hunter handoff

- Last updated: 2026-05-21T13:08:08Z
- Started: 2026-05-21T12:19:25Z
- Ended: 2026-05-21T13:08:08Z
- Measured minutes: 48.72
- Primary outcome: regression_rows_emitted
- Rule under attack: materializer equivalence on local geometry prefilters plus later-offset source-valid ePK entity v4 seed coverage; regression gate for ATPase/transporter/ORC-MCM/motor/same-chain/internal-fragment/ligand-materialization controls.
- Production claim allowed: false
- Labels/fingerprints changed: false

## Search Surface

Ran the next-query gap audit plus later-offset source-valid entity seed expansion. CIFs were fetched in memory only and reduced to compact summaries.

- Full helper artifact: `artifacts/research_lanes/epk_false_positive_hunter/source_valid_later_offset_gap_audit_20260521_121925Z.json`
- JNK-family retry artifact: `artifacts/research_lanes/epk_false_positive_hunter/source_valid_later_offset_gap_audit_jnk_entity_retry_20260521_121925Z.json`
- Extended regression gate: `artifacts/research_lanes/epk_false_positive_hunter/epk_candidate_evidence_v1_regression_gate_20260521_130730Z.json`
- Helpers: `tools/research_lanes/epk_false_positive_hunter/source_valid_later_offset_gap_audit.py`, `tools/research_lanes/epk_false_positive_hunter/epk_candidate_evidence_regression_gate.py`
- Full pass reviewed 307 entries / 657 coordinate contexts; retry reviewed 124 entries / 273 coordinate contexts.
- Materializer contexts: 8 in the full pass, 13 in the retry.
- Fetch errors: 0
- Materializer context errors: 0
- Raw coordinate files written: false

## Result

No new unsafe ePK non-abstention was found on this bounded surface.

- `8OOZ`, `9OFD`, `9OFE`, and `9W1G` deposited and biological assembly contexts all had local gamma-to-acceptor geometry, but all eight materializer probes abstained.
- The gap is explained by heteromeric entity mapping: every audited local hit mapped acceptor and gamma-associated polymer to the same author chain and same entity.
- The full later-offset CDK/JNK/RTK/mTOR text/component surface found no source-valid v4 seed under the prior family bucket heuristic.
- A lane-only JNK heuristic expansion recognized `MITOGEN-ACTIVATED PROTEIN KINASE 8` as `jnk_entity`; bounded retry promoted `4UX9` as a source-valid later-offset v4 seed beyond `9LGO`.
- `4UX9` produced five deposited/assembly materializer contexts and all returned `source_valid_epk_seed_no_substrate_mode_materializer_hit_review_only`.
- The new regression gate emitted 318 `epk_candidate_evidence_v1` rows. Expected-policy unsafe non-abstentions stayed 0.
- The pinned context-v4-only assembly split failure remains `5UJ7:biological_assembly_1`.

## Evidence For / Against

Evidence for the regression gate extension:

- Added eight `materializer_equivalence_gap_same_chain_entity_control` rows for the local-geometry/materializer-equivalence gap.
- Added five `source_valid_later_offset_epk_seed_overblock_control` rows for `4UX9`.
- Preserved coordinate state, deposited/assembly context, guard state, expected/observed materializer decision, and candidate geometry where available.

Evidence against counterexamples on this run's surface:

- No gap-audit context had a heteromeric entity-eligible local geometry hit.
- No later-offset source-valid seed materialized an unsafe substrate-mode hit.
- The 318-row gate still has `unsafe_nonabstention_after_expected_policy_count=0`.

## Verification

Pending final wrap verification after this handoff update:

- JSON validation for new artifacts and ledger.
- `py_compile` for changed helpers.
- `git diff --check` on lane files.

## Blockers

- `git fetch origin` failed writing linked-worktree `FETCH_HEAD`: Operation not permitted.
- `git pull --ff-only origin research/epk-false-positive-hunter` failed writing linked-worktree `FETCH_HEAD`: Operation not permitted.
- `git fetch --no-write-fetch-head origin` succeeded.
- Normal checked-out HEAD was behind origin at run start because linked-worktree metadata writes remain blocked.

## Next Query

Run a full later-offset retry with expanded family buckets and stronger polymer-entity/title fallback for RTK, EGFR, CDK/cyclin, mTORC1/2, and JNK; prioritize source-valid deposited-or-assembly v4 positives beyond `4UX9` and `9LGO`, then join any hits into the regression gate. Keep production labels, thresholds, registries/fingerprints, migrations, and scoring forbidden.

Production claims, label changes, threshold calibration, registry/fingerprint edits, artifact migrations, and production scoring remain forbidden.

## Files Changed

- `tools/research_lanes/epk_false_positive_hunter/source_valid_epk_seed_geometry_prefilter_stress.py`
- `tools/research_lanes/epk_false_positive_hunter/epk_candidate_evidence_regression_gate.py`
- `artifacts/research_lanes/epk_false_positive_hunter/source_valid_later_offset_gap_audit_20260521_121925Z.json`
- `artifacts/research_lanes/epk_false_positive_hunter/source_valid_later_offset_gap_audit_jnk_entity_retry_20260521_121925Z.json`
- `artifacts/research_lanes/epk_false_positive_hunter/epk_candidate_evidence_v1_regression_gate_20260521_130730Z.json`
- `artifacts/research_lanes/epk_false_positive_hunter/epk_false_positive_hunter_runs.jsonl`
- `work/research_lanes/epk_false_positive_hunter/handoff.md`
