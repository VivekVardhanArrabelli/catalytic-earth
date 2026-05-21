# ePK false-positive hunter handoff

- Last updated: 2026-05-21T03:39:39Z
- Started: 2026-05-21T03:30:57Z
- Ended: 2026-05-21T03:39:39Z
- Measured minutes: 8.70
- Primary outcome: regression_rows_emitted
- Pushed commit: b06cffc043c1dd7e713d70a4179be59cadd15258 via alternate-index commit/push.
- Rule under attack: current materializer non-abstention on ATPase/transporter/ORC-MCM/motor/same-chain/internal-fragment/namespace controls and assembly-context v4 sufficiency.
- Production claim allowed: false
- Labels/fingerprints changed: false

## Search Surface

Converted recent false-positive hunter artifacts into lane-only `epk_candidate_evidence_v1`-style regression rows. This run did not fetch or write raw coordinates.

- Helper: `tools/research_lanes/epk_false_positive_hunter/epk_candidate_evidence_regression_gate.py`
- Primary artifact: `artifacts/research_lanes/epk_false_positive_hunter/epk_candidate_evidence_v1_regression_gate_20260521_033057Z.json`
- Source artifacts consumed: 10
- Source rows converted: 295
- Regression rows emitted: 295
- Control classes covered: ATPase/transporter, Walker-A/internal-fragment, non-ePK ATP/Mg enzymes, ORC/MCM deposited and biological assembly controls, same-chain/entity-reuse controls, gamma-chain namespace controls, ligand materialization no-hit controls, auth/label gamma collision counterexamples, and source-context ePK overblock controls.

## Result

The 5UJ7 biological assembly residual is now a concrete regression fixture row.

- `5UJ7:biological_assembly_1` is pinned as `orc_mcm_biological_assembly_split_control`.
- Coordinate state: biological assembly.
- Candidate: TYR174 chain C OH to ATP PG associated with chain A at 5.822 A.
- Context guard: assembly-context v4 is false; deposited-v4/below-chain-floor split is true.
- Topology: same-chain and reciprocal topology flags are false.
- Observed materializer decision: topology-clear substrate-mode non-abstention.
- Expected policy decision: block or abstain as a non-ePK ORC/MCM control.
- Blocker row: `entry_level_any_context_v4_review_only`.

The regression gate artifact distinguishes raw materializer pressure from policy safety:

- Observed topology-clear non-ePK materializer non-abstentions: 82 review-only pressure rows.
- Unsafe non-abstentions after expected policy blockers: 0.
- Context-v4-only unsafe non-abstentions: 1, `5UJ7:biological_assembly_1`.
- Biological-assembly split materializer counterexamples: 1, `5UJ7:biological_assembly_1`.
- Split rows `1A49:biological_assembly_1`, `1A49:biological_assembly_2`, `1A5U:biological_assembly_1`, and `1A5U:biological_assembly_2` carried no substrate-mode materializer hit.

## Evidence For / Against

Evidence for the regression fixture:

- The converter preserved candidate-level coordinate state, gamma/acceptor details, context/deposited guard state, topology flags, blocker class, expected policy decision, and observed materializer decision for 295 rows.
- The emitted gate explicitly falsifies context-v4-only sufficiency via 5UJ7 while keeping the expected-policy regression gate at zero unsafe non-abstentions.

Evidence against broader assembly split residuals on the converted source surface:

- No deposited-v4 / biological-assembly split materializer counterexample beyond 5UJ7 appeared in the 20 assembly-guard materializer rows converted from the deep pass.
- The 121 ePK-query non-ePK contaminant materializer rows remained no-hit controls in the emitted gate.

## Verification

- `python -m json.tool artifacts/research_lanes/epk_false_positive_hunter/epk_candidate_evidence_v1_regression_gate_20260521_033057Z.json >/dev/null`
- `python -m py_compile tools/research_lanes/epk_false_positive_hunter/epk_candidate_evidence_regression_gate.py`
- `git diff --check -- tools/research_lanes/epk_false_positive_hunter/epk_candidate_evidence_regression_gate.py artifacts/research_lanes/epk_false_positive_hunter/epk_candidate_evidence_v1_regression_gate_20260521_033057Z.json`

## Blockers

- `git fetch origin` failed writing linked-worktree `FETCH_HEAD`: Operation not permitted.
- `git pull --ff-only origin research/epk-false-positive-hunter` failed writing linked-worktree `FETCH_HEAD`: Operation not permitted.
- `git fetch --no-write-fetch-head origin` succeeded.
- Local checked-out HEAD remains behind `origin/research/epk-false-positive-hunter`; normal status still reflects linked-worktree index metadata issues from prior runs.

## Next Query

Use the emitted regression gate as the negative-control substrate for a source-valid ePK seed search: build kinase-classified polymer/entity evidence for RAF/MEK/ERK, JNK, CDK/cyclin, receptor tyrosine kinase dimer, and mTORC1/2 ATP/ANP assemblies, force deposited and biological-assembly contexts through the materializer, and join results against `epk_candidate_evidence_v1` rows. In parallel, prefilter non-ePK v4 contaminants for local Tyr or N-terminal Ser/Thr/Tyr gamma geometry before materialization. Keep production labels, thresholds, registries/fingerprints, migrations, and scoring forbidden.

Production claims, label changes, threshold calibration, registry/fingerprint edits, artifact migrations, and production scoring remain forbidden.

## Files Changed

- `tools/research_lanes/epk_false_positive_hunter/epk_candidate_evidence_regression_gate.py`
- `artifacts/research_lanes/epk_false_positive_hunter/epk_candidate_evidence_v1_regression_gate_20260521_033057Z.json`
- `artifacts/research_lanes/epk_false_positive_hunter/epk_false_positive_hunter_runs.jsonl`
- `work/research_lanes/epk_false_positive_hunter/handoff.md`

The alternate-index commit also preserves prior generated lane outputs that were
present in the worktree and used as source inputs but still absent from the
fetched remote ref:

- `tools/research_lanes/epk_false_positive_hunter/v4_entry_level_epk_overblock_later_offset_stress.py`
- `artifacts/research_lanes/epk_false_positive_hunter/v4_entry_level_epk_overblock_later_offset_stress_20260521_023614Z.json`
- `artifacts/research_lanes/epk_false_positive_hunter/v4_entry_level_epk_overblock_later_offset_stress_targeted_20260521_025652Z.json`
- `artifacts/research_lanes/epk_false_positive_hunter/v4_entry_level_epk_overblock_later_offset_contaminant_stress_20260521_030753Z.json`
