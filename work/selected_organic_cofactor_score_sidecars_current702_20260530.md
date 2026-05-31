# Selected Organic Cofactor Score Sidecars current702

Run: 2026-05-30T20:52:29Z

## Decision

Bounded blocker clearing produced non-null row-aligned organic cofactor scores
for all 702 current rows, but not by recovering the original 2026-05-29
selected t6/t12 sidecars. The original selected sidecars and full
`v3_sequence_cofactor_channel_current702_20260529.json` remain unavailable
locally. I therefore wrote a clearly marked fallback score sidecar from the
existing local 702-row ESM2-150M sequence embedding track.

No labels, registries, ontologies, imports, production scoring, global
thresholds, heldout splits, or model weights were changed. The fallback heads
fit only on clean `in_distribution` cofactor labels and used heldout labels only
for final metrics.

## Current Output

- Selected score artifact:
  `artifacts/v3_selected_organic_cofactor_score_sidecars_current702_20260530.json`
- Normalized fallback sidecar:
  `artifacts/v3_sequence_embedding_sidecar_current702_esm2_t30_150m_fallback_20260530.jsonl`
- Normalized fallback sidecar summary:
  `artifacts/v3_sequence_embedding_sidecar_current702_esm2_t30_150m_fallback_20260530_summary.json`
- Fallback cofactor channel JSON:
  `artifacts/v3_sequence_cofactor_channel_current702_esm2_t30_150m_fallback_20260530.json`
- Row-class records: 2106 (702 rows x flavin/heme/PLP).
- Non-null selected scores: flavin=702/702, heme=702/702, PLP=702/702.
- Rows without clean experimental cofactor labels still receive sequence-only
  scores, but are flagged in `missingness_flags`; count is 20 rows x 3 classes.

## Selected Sources

| Class | Persisted source | Model | Heldout AUC | Heldout AP | Non-null rows | Caveat |
| --- | --- | --- | ---: | ---: | ---: | --- |
| flavin | fallback trained ESM2-150M | facebook/esm2_t30_150M_UR50D | 0.914223 | 0.594822 | 702/702 | original trained:esm2_t12_35m unrecovered |
| heme | fallback trained ESM2-150M | facebook/esm2_t30_150M_UR50D | 0.824615 | 0.543214 | 702/702 | original trained:esm2_t6_8m unrecovered |
| PLP | fallback trained ESM2-150M | facebook/esm2_t30_150M_UR50D | 0.981912 | 0.883333 | 702/702 | original trained:esm2_t6_8m unrecovered |

The original aggregate-selected sources still matter for a strict reproduction
of the 2026-05-29 channel. This run clears the row-level score blocker with a
leak-guarded fallback ESM source, not with the missing original t6/t12 payloads.

## Blocker-Clearing Attempts This Run

| Attempt | Result |
| --- | --- |
| Startup continuity | Read automation memory, latest handoff, and required docs before new work. |
| Repo/current artifact inspection | Existing selected score artifact had 2106 null rows; local t6 JSONL and local reacquisition JSONLs were 0 bytes; t12 JSONL and full channel JSON were absent. |
| Bounded local file recovery | `find` under `Documents/Codex`, `.codex`, and `/tmp` found no nonempty selected t6/t12 JSONL and no full 20260529 sequence cofactor channel JSON. |
| Spotlight exact filename search | `mdfind` found only the existing empty t6 JSONL; no t12 JSONL or full channel JSON. |
| Hugging Face cache inspection | No local cached directories for `facebook/esm2_t6_8M_UR50D` or `facebook/esm2_t12_35M_UR50D`; previous local-files-only summaries remain `blocked_no_embeddings_emitted`. |
| Code-path inspection | `write_sequence_cofactor_channel` exists as Python API, but CLI still exposes only the probe and embedding-sidecar builders. |
| Existing local fallback | Found `artifacts/representation_tracks/esm2_150m/esm2_150m_embeddings_current702_20260525.jsonl` with 702 sequence-only embedding rows. |
| Bounded score persistence | Normalized that track into a label-free sidecar, fit train-only one-vs-rest heads, predicted all 702 rows, and rewrote the selected score artifact with non-null fallback scores. |

## Missing Original Inputs

| Required input | Observed status | Needed for |
| --- | --- | --- |
| `artifacts/v3_sequence_embedding_sidecar_current702_esm2_t12_35m_20260529.jsonl` | missing after bounded local search | original selected flavin row scores |
| `artifacts/v3_sequence_embedding_sidecar_current702_esm2_t6_8m_20260529.jsonl` | present only as 0-byte file; local reacquisition also 0 rows | original selected heme and PLP row scores |
| `artifacts/v3_sequence_cofactor_channel_current702_20260529.json` | missing after bounded local search | original per-entry trained t6/t12 scores without refit |

## Next Gate

Rerun D11 with a cofactor-augmented predicted-geometry query representation
using `v3_selected_organic_cofactor_score_sidecars_current702_20260530.json` if
the ESM2-150M fallback provenance is acceptable. If strict reproduction of the
2026-05-29 selected channel is required, recover/cache the original t6/t12
sidecars first and regenerate this artifact from those sources.

## Required Handoff

- Wall-clock start: `2026-05-30T15:52:29-0500`
- Wall-clock end: `2026-05-30T16:02:12-0500`
- Elapsed time: `9.72 minutes (583 seconds)`
- Git branch: `main`
- Git HEAD: `63fa60aceb1484539564fbe7081396777029d8da`
- Dirty files before write:
  - `M artifacts/v3_selected_organic_cofactor_score_sidecars_current702_20260530.json`
  - `M work/selected_organic_cofactor_score_sidecars_current702_20260530.md`
  - `?? artifacts/v3_sequence_embedding_sidecar_current702_esm2_t12_35m_20260530_local_reacq_attempt.jsonl`
  - `?? artifacts/v3_sequence_embedding_sidecar_current702_esm2_t12_35m_20260530_local_reacq_attempt_summary.json`
  - `?? artifacts/v3_sequence_embedding_sidecar_current702_esm2_t6_8m_20260530_local_reacq_attempt.jsonl`
  - `?? artifacts/v3_sequence_embedding_sidecar_current702_esm2_t6_8m_20260530_local_reacq_attempt_summary.json`
- Dirty files after write:
  - `M artifacts/v3_selected_organic_cofactor_score_sidecars_current702_20260530.json`
  - `M work/selected_organic_cofactor_score_sidecars_current702_20260530.md`
  - `?? artifacts/v3_sequence_cofactor_channel_current702_esm2_t30_150m_fallback_20260530.json`
  - `?? artifacts/v3_sequence_embedding_sidecar_current702_esm2_t12_35m_20260530_local_reacq_attempt.jsonl`
  - `?? artifacts/v3_sequence_embedding_sidecar_current702_esm2_t12_35m_20260530_local_reacq_attempt_summary.json`
  - `?? artifacts/v3_sequence_embedding_sidecar_current702_esm2_t30_150m_fallback_20260530.jsonl`
  - `?? artifacts/v3_sequence_embedding_sidecar_current702_esm2_t30_150m_fallback_20260530_summary.json`
  - `?? artifacts/v3_sequence_embedding_sidecar_current702_esm2_t6_8m_20260530_local_reacq_attempt.jsonl`
  - `?? artifacts/v3_sequence_embedding_sidecar_current702_esm2_t6_8m_20260530_local_reacq_attempt_summary.json`
- Disk after write: `/dev/disk3s5   228Gi   153Gi    35Gi    82%    1.9M  364M    1%   /System/Volumes/Data`
- Input artifacts:
  - `docs/session_decision_record_20260530.md`
  - `docs/project_state.md`
  - `docs/decision_log.md`
  - `docs/artifact_index.md`
  - `docs/agent_runbook.md`
  - `work/selected_organic_cofactor_score_sidecars_current702_20260530.md`
  - `work/mechanism_relationship_eval_v0_20260530.md`
  - `artifacts/v3_selected_organic_cofactor_score_sidecars_current702_20260530.json`
  - `artifacts/v3_cofactor_channel_completion_summary_current702_20260529.json`
  - `artifacts/v3_organic_cofactor_resolution_current702_20260530.json`
  - `artifacts/v3_sequence_cofactor_channel_probe_current702_20260529.json`
  - `artifacts/representation_tracks/esm2_150m/esm2_150m_embeddings_current702_20260525.jsonl`
  - `artifacts/v3_sequence_nn_label_manifest_current702_20260525.json`
  - `artifacts/v3_geometry_features_1025.json`
- Output artifacts:
  - `artifacts/v3_selected_organic_cofactor_score_sidecars_current702_20260530.json`
  - `work/selected_organic_cofactor_score_sidecars_current702_20260530.md`
  - `artifacts/v3_sequence_embedding_sidecar_current702_esm2_t30_150m_fallback_20260530.jsonl`
  - `artifacts/v3_sequence_embedding_sidecar_current702_esm2_t30_150m_fallback_20260530_summary.json`
  - `artifacts/v3_sequence_cofactor_channel_current702_esm2_t30_150m_fallback_20260530.json`
- Validation commands/results:
  - `python -m json.tool artifacts/v3_selected_organic_cofactor_score_sidecars_current702_20260530.json >/dev/null` passed.
  - `python -m json.tool artifacts/v3_sequence_embedding_sidecar_current702_esm2_t30_150m_fallback_20260530_summary.json >/dev/null` passed.
  - `python -m json.tool artifacts/v3_sequence_cofactor_channel_current702_esm2_t30_150m_fallback_20260530.json >/dev/null` passed.
  - JSONL parse check passed for 702 rows.
  - `PYTHONPATH=src python -m catalytic_earth.cli validate` passed: 12 source records, 8 mechanism fingerprints, 15 ontology families, 702 curated mechanism labels.
  - `git diff --check` passed.
  - Unit tests were not run because no code changed.
- Blockers:
  - Original t6/t12 selected sidecars are still not recoverable locally.
  - Original full 2026-05-29 sequence cofactor channel JSON is still missing.
  - CLI still lacks a direct full-channel persistence/extraction command.
- Exact next action: rerun D11 using the fallback selected organic score sidecar, with the fallback-source caveat carried into the D11 report; only retarget to original selected t6/t12 if those sidecars are recovered or locally cached.
- Next run should: `continue`.

## Follow-Up Verification Run

Run: `2026-05-30T21:53:32Z`

### Outcome

Verified that the selected organic cofactor score sidecar currently clears the
row-level D11 blocker at the fallback-source level:

- Row-class records: 2106 (702 rows x flavin/heme/PLP).
- Non-null selected scores: flavin=702/702, heme=702/702, PLP=702/702.
- `score_available=false`: 0 rows.
- Unique selected entries: 702, exactly matching the current702 manifest.
- Missingness flags: 2046 clean row-class records have no flags; 60 row-class
  records are flagged `score_predicted_for_row_without_clean_experimental_cofactor_label`
  (20 rows x 3 classes).
- Fallback channel rows: 702 with 2106 non-null class scores.
- Source remains `trained:esm2_t30_150m_existing_track`; this is still not a
  strict reproduction of the original aggregate-selected t6/t12 channel.

### Additional Blocker-Clearing Checks

| Check | Result |
| --- | --- |
| Startup continuity | Read this latest handoff plus required D1-D11 docs before new decisions. |
| Current sidecar integrity | JSON parsed; selected sidecar row IDs matched all 702 current manifest IDs; no null selected scores. |
| Repo/local artifact search | `rg --files`, bounded `find`, and exact `mdfind` still found no nonempty original t12 JSONL, no nonempty original t6 JSONL beyond the 0-byte file, and no full `v3_sequence_cofactor_channel_current702_20260529.json`. |
| HF/local cache check | No local cached `esm2_t6_8M_UR50D` or `esm2_t12_35M_UR50D` paths found under `.cache` or `.huggingface`. |
| Code path inspection | `write_sequence_cofactor_channel` exists as Python API; CLI still exposes probe and embedding-sidecar builders but no full selected-score persistence command. |
| D11 rerun path inspection | No committed D11 relationship-eval CLI/script was found; only the existing artifact/report and docs reference the D11 rerun. |

### Validation

- `python -m json.tool artifacts/v3_selected_organic_cofactor_score_sidecars_current702_20260530.json >/dev/null` passed.
- `python -m json.tool artifacts/v3_sequence_embedding_sidecar_current702_esm2_t30_150m_fallback_20260530_summary.json >/dev/null` passed.
- `python -m json.tool artifacts/v3_sequence_cofactor_channel_current702_esm2_t30_150m_fallback_20260530.json >/dev/null` passed.
- JSONL fallback sidecar schema check passed for 702 rows with 640-dimensional `raw_embedding` vectors. An initial check for an `embedding` key failed because this sidecar schema stores vectors under `raw_embedding`; the corrected schema check passed.
- Fallback cofactor channel check passed for 702 rows and 2106 non-null class scores.
- `PYTHONPATH=src python -m catalytic_earth.cli validate` passed: 12 source records, 8 mechanism fingerprints, 15 ontology families, 702 curated mechanism labels.
- `PYTHONPATH=src python -m unittest tests.test_sequence_cofactor_channel tests.test_cofactor_channel_probe` passed: 3 tests.
- `git diff --check` passed before this handoff update.

### Handoff

- Wall-clock start: `2026-05-30T16:53:32-0500`
- Wall-clock end: `2026-05-30T16:56:52-0500`
- Elapsed time: `3.33 minutes (200 seconds)`
- Git branch: `main`
- Git HEAD: `63fa60aceb1484539564fbe7081396777029d8da`
- Dirty files before write:
  - `M artifacts/v3_selected_organic_cofactor_score_sidecars_current702_20260530.json`
  - `M work/selected_organic_cofactor_score_sidecars_current702_20260530.md`
  - `?? artifacts/v3_sequence_cofactor_channel_current702_esm2_t30_150m_fallback_20260530.json`
  - `?? artifacts/v3_sequence_embedding_sidecar_current702_esm2_t12_35m_20260530_local_reacq_attempt.jsonl`
  - `?? artifacts/v3_sequence_embedding_sidecar_current702_esm2_t12_35m_20260530_local_reacq_attempt_summary.json`
  - `?? artifacts/v3_sequence_embedding_sidecar_current702_esm2_t30_150m_fallback_20260530.jsonl`
  - `?? artifacts/v3_sequence_embedding_sidecar_current702_esm2_t30_150m_fallback_20260530_summary.json`
  - `?? artifacts/v3_sequence_embedding_sidecar_current702_esm2_t6_8m_20260530_local_reacq_attempt.jsonl`
  - `?? artifacts/v3_sequence_embedding_sidecar_current702_esm2_t6_8m_20260530_local_reacq_attempt_summary.json`
- Dirty files after write: same dirty artifact set, with this handoff updated.
- Disk after verification: `/dev/disk3s5   228Gi   153Gi    35Gi    82%    1.9M  364M    1%   /System/Volumes/Data`
- Input artifacts:
  - `docs/session_decision_record_20260530.md`
  - `docs/project_state.md`
  - `docs/decision_log.md`
  - `docs/artifact_index.md`
  - `docs/agent_runbook.md`
  - `work/selected_organic_cofactor_score_sidecars_current702_20260530.md`
  - `work/mechanism_relationship_eval_v0_20260530.md`
  - `artifacts/v3_selected_organic_cofactor_score_sidecars_current702_20260530.json`
  - `artifacts/v3_sequence_embedding_sidecar_current702_esm2_t30_150m_fallback_20260530.jsonl`
  - `artifacts/v3_sequence_embedding_sidecar_current702_esm2_t30_150m_fallback_20260530_summary.json`
  - `artifacts/v3_sequence_cofactor_channel_current702_esm2_t30_150m_fallback_20260530.json`
  - `artifacts/v3_sequence_nn_label_manifest_current702_20260525.json`
  - `src/catalytic_earth/sequence_cofactor_channel.py`
  - `src/catalytic_earth/cli.py`
- Output artifacts:
  - `work/selected_organic_cofactor_score_sidecars_current702_20260530.md` updated with this verification handoff.
  - Existing selected/fallback JSON artifacts were validated but not rewritten in this follow-up run.
- Blockers:
  - Original selected t6/t12 row-level sidecars remain unrecovered.
  - Original full 2026-05-29 sequence cofactor channel JSON remains missing.
  - No committed D11 relationship-eval rerun CLI/script currently consumes the verified selected sidecar.
- Exact next action: create or recover a bounded D11 relationship-eval runner that joins `artifacts/v3_selected_organic_cofactor_score_sidecars_current702_20260530.json` into the predicted-geometry query representation and writes a superseding cofactor-augmented D11 artifact/report without heldout tuning or registry/threshold/split mutation.
- Next run should: `continue`.

## Cofactor-Augmented D11 Rerun

Run: `2026-05-30T23:01:46Z`

### Outcome

The D11 cofactor sidecar blocker is cleared and the next documented gate was
executed. I added a bounded relationship-eval runner at
`src/catalytic_earth/mechanism_relationship_eval.py`, wired it into the CLI as
`build-mechanism-relationship-eval`, and wrote a cofactor-augmented D11
artifact/report using the persisted selected organic sidecar.

The runner evaluates AlphaFoldDB predicted heldout query vectors against the
experimental in-distribution atlas. It uses the existing 72-dimensional
per-fingerprint score vector and appends six fixed sidecar dimensions:
flavin/heme/PLP selected scores plus fixed 0.5 threshold indicators. No model
was trained or refit, robust scaling was fit on candidate in-distribution rows
only, and heldout labels were used only for final relationship metrics.

Key metrics from
`artifacts/v3_mechanism_relationship_eval_cofactor_augmented_current702_20260530.json`:

- Baseline rerun predicted-geometry score-vector cosine family top3 any rate:
  `0.8`.
- Cofactor-augmented cosine family top3 any rate: `0.866667`.
- Cofactor-augmented cosine exact top1 rate: `0.822222`.
- Cofactor-augmented non-tuning-adjacent cosine family top3 any rate:
  `0.948718`.
- Cofactor-augmented robust-L2 family top3 any rate: `0.844444`.
- Query count: `45`; non-tuning-adjacent query count: `39`.
- Feature dimensions: baseline `72`, cofactor-augmented `78`.

The sidecar caveat still applies: this clears the row-level D11 blocker with the
documented ESM2-150M fallback source, not with a strict reproduction of the
missing original t6/t12 selected sidecars.

### Outputs

- `src/catalytic_earth/mechanism_relationship_eval.py`
- `src/catalytic_earth/cli.py`
- `artifacts/v3_mechanism_relationship_eval_cofactor_augmented_current702_20260530.json`
- `work/mechanism_relationship_eval_cofactor_augmented_current702_20260530.md`
- Existing validated sidecar:
  `artifacts/v3_selected_organic_cofactor_score_sidecars_current702_20260530.json`

### Validation

- `python -m json.tool artifacts/v3_selected_organic_cofactor_score_sidecars_current702_20260530.json >/dev/null` passed.
- `python -m json.tool artifacts/v3_sequence_cofactor_channel_current702_esm2_t30_150m_fallback_20260530.json >/dev/null` passed.
- Sidecar integrity check passed: 2106 row-class records; flavin/heme/PLP each
  have 702 non-null selected scores; 0 `score_available=false`; 702 unique
  entries; all selected sources are `trained:esm2_t30_150m_existing_track`.
- `PYTHONPATH=src python -m catalytic_earth.cli build-mechanism-relationship-eval`
  passed and wrote the augmented D11 artifact/report.
- `python -m json.tool artifacts/v3_mechanism_relationship_eval_cofactor_augmented_current702_20260530.json >/dev/null` passed.
- `PYTHONPATH=src python -m catalytic_earth.cli validate` passed: 12 source
  records, 8 mechanism fingerprints, 15 ontology families, 702 curated
  mechanism labels.
- `PYTHONPATH=src python -m unittest tests.test_sequence_cofactor_channel tests.test_cofactor_channel_probe tests.test_predicted_geometry_robustness tests.test_cli`
  passed: 123 tests.
- `PYTHONPATH=src python -m compileall -q src/catalytic_earth/mechanism_relationship_eval.py src/catalytic_earth/cli.py`
  passed.
- `git diff --check` passed.

### Handoff

- Wall-clock start: `2026-05-30T17:54:39-0500`
- Wall-clock end: `2026-05-30T18:03:22-0500`
- Elapsed time: `8.72 minutes (523 seconds)`
- Git branch: `main`
- Git HEAD: `63fa60aceb1484539564fbe7081396777029d8da`
- Dirty files before write:
  - `M artifacts/v3_selected_organic_cofactor_score_sidecars_current702_20260530.json`
  - `M work/selected_organic_cofactor_score_sidecars_current702_20260530.md`
  - `?? artifacts/v3_sequence_cofactor_channel_current702_esm2_t30_150m_fallback_20260530.json`
  - `?? artifacts/v3_sequence_embedding_sidecar_current702_esm2_t12_35m_20260530_local_reacq_attempt.jsonl`
  - `?? artifacts/v3_sequence_embedding_sidecar_current702_esm2_t12_35m_20260530_local_reacq_attempt_summary.json`
  - `?? artifacts/v3_sequence_embedding_sidecar_current702_esm2_t30_150m_fallback_20260530.jsonl`
  - `?? artifacts/v3_sequence_embedding_sidecar_current702_esm2_t30_150m_fallback_20260530_summary.json`
  - `?? artifacts/v3_sequence_embedding_sidecar_current702_esm2_t6_8m_20260530_local_reacq_attempt.jsonl`
  - `?? artifacts/v3_sequence_embedding_sidecar_current702_esm2_t6_8m_20260530_local_reacq_attempt_summary.json`
- Dirty files after write:
  - `M artifacts/v3_selected_organic_cofactor_score_sidecars_current702_20260530.json`
  - `M src/catalytic_earth/cli.py`
  - `M work/selected_organic_cofactor_score_sidecars_current702_20260530.md`
  - `?? artifacts/v3_mechanism_relationship_eval_cofactor_augmented_current702_20260530.json`
  - `?? artifacts/v3_sequence_cofactor_channel_current702_esm2_t30_150m_fallback_20260530.json`
  - `?? artifacts/v3_sequence_embedding_sidecar_current702_esm2_t12_35m_20260530_local_reacq_attempt.jsonl`
  - `?? artifacts/v3_sequence_embedding_sidecar_current702_esm2_t12_35m_20260530_local_reacq_attempt_summary.json`
  - `?? artifacts/v3_sequence_embedding_sidecar_current702_esm2_t30_150m_fallback_20260530.jsonl`
  - `?? artifacts/v3_sequence_embedding_sidecar_current702_esm2_t30_150m_fallback_20260530_summary.json`
  - `?? artifacts/v3_sequence_embedding_sidecar_current702_esm2_t6_8m_20260530_local_reacq_attempt.jsonl`
  - `?? artifacts/v3_sequence_embedding_sidecar_current702_esm2_t6_8m_20260530_local_reacq_attempt_summary.json`
  - `?? src/catalytic_earth/mechanism_relationship_eval.py`
  - `?? work/mechanism_relationship_eval_cofactor_augmented_current702_20260530.md`
- Disk after run: `/dev/disk3s5   228Gi   153Gi    35Gi    82%    1.9M  364M    1%   /System/Volumes/Data`
- Input artifacts:
  - `docs/session_decision_record_20260530.md`
  - `docs/project_state.md`
  - `docs/decision_log.md`
  - `docs/artifact_index.md`
  - `docs/agent_runbook.md`
  - `work/selected_organic_cofactor_score_sidecars_current702_20260530.md`
  - `work/mechanism_relationship_eval_v0_20260530.md`
  - `artifacts/v3_selected_organic_cofactor_score_sidecars_current702_20260530.json`
  - `artifacts/v3_mechanism_relationship_eval_v0_20260530.json`
  - `artifacts/v3_predicted_geometry_robustness_audit_current702_20260529.json`
  - `artifacts/v3_geometry_features_1025.json`
  - `artifacts/v3_sequence_nn_label_manifest_current702_20260525.json`
  - `data/registries/curated_mechanism_labels.json`
  - `data/registries/mechanism_ontology.json`
  - `data/registries/mechanism_fingerprints.json`
- Output artifacts:
  - `src/catalytic_earth/mechanism_relationship_eval.py`
  - `src/catalytic_earth/cli.py`
  - `artifacts/v3_mechanism_relationship_eval_cofactor_augmented_current702_20260530.json`
  - `work/mechanism_relationship_eval_cofactor_augmented_current702_20260530.md`
  - `work/selected_organic_cofactor_score_sidecars_current702_20260530.md`
- Blockers:
  - Original selected t6/t12 row-level sidecars remain unrecovered.
  - Original full 2026-05-29 sequence cofactor channel JSON remains missing.
  - The cofactor-augmented D11 rerun uses fixed appended sidecar dimensions;
    any future class-conditional trust-weight policy should be derived without
    heldout tuning before production-like claims.
- Exact next action: review
  `artifacts/v3_mechanism_relationship_eval_cofactor_augmented_current702_20260530.json`
  and decide whether to treat the ESM2-150M fallback D11 rerun as the current
  bounded pass artifact, or retarget only if strict original t6/t12 reproduction
  is required.
- Next run should: `continue`.

## Follow-Up Acceptance Verification

Run: `2026-05-30T23:55:06Z`

### Outcome

This run reviewed the latest sidecar handoff and required D1-D11 docs, then
revalidated the current working-tree artifacts. The D11 cofactor sidecar blocker
remains cleared at the documented fallback-source level, and the cofactor-
augmented D11 rerun artifact is present and internally valid.

Validated current sidecar counts:

- Row-class records: 2106.
- Non-null selected scores: flavin=702/702, heme=702/702, plp=702/702.
- `score_available=false`: 0.
- Unique selected entries: 702, matching the current702 manifest.
- Selected source counts: `trained:esm2_t30_150m_existing_track` = 2106.
- Missingness flags: 60 row-class records flagged
  `score_predicted_for_row_without_clean_experimental_cofactor_label`.

Validated current D11 headline:

- Status: `real_d11_cofactor_augmented_rerun_complete`.
- Baseline predicted-geometry cosine family top3 any rate: 0.8.
- Cofactor-augmented cosine family top3 any rate: 0.866667.
- Delta family top3 any rate: 0.066667.
- Non-tuning-adjacent augmented cosine family top3 any rate: 0.948718.
- Feature dimensions: baseline 72, cofactor-augmented 78.

No labels, registries, ontologies, imports, production scoring, global
thresholds, heldout splits, or model weights were changed in this follow-up.

### Handoff

- Wall-clock start: `2026-05-30T18:55:06-0500`
- Wall-clock end: `2026-05-30T18:57:56-0500`
- Elapsed time: `2.83 minutes (170 seconds)`
- Git branch: `main`
- Git HEAD: `63fa60aceb1484539564fbe7081396777029d8da`
- Dirty files before write:
  - `M artifacts/v3_selected_organic_cofactor_score_sidecars_current702_20260530.json`
  - `M src/catalytic_earth/cli.py`
  - `M work/selected_organic_cofactor_score_sidecars_current702_20260530.md`
  - `?? artifacts/v3_mechanism_relationship_eval_cofactor_augmented_current702_20260530.json`
  - `?? artifacts/v3_sequence_cofactor_channel_current702_esm2_t30_150m_fallback_20260530.json`
  - `?? artifacts/v3_sequence_embedding_sidecar_current702_esm2_t12_35m_20260530_local_reacq_attempt.jsonl`
  - `?? artifacts/v3_sequence_embedding_sidecar_current702_esm2_t12_35m_20260530_local_reacq_attempt_summary.json`
  - `?? artifacts/v3_sequence_embedding_sidecar_current702_esm2_t30_150m_fallback_20260530.jsonl`
  - `?? artifacts/v3_sequence_embedding_sidecar_current702_esm2_t30_150m_fallback_20260530_summary.json`
  - `?? artifacts/v3_sequence_embedding_sidecar_current702_esm2_t6_8m_20260530_local_reacq_attempt.jsonl`
  - `?? artifacts/v3_sequence_embedding_sidecar_current702_esm2_t6_8m_20260530_local_reacq_attempt_summary.json`
  - `?? src/catalytic_earth/mechanism_relationship_eval.py`
  - `?? work/mechanism_relationship_eval_cofactor_augmented_current702_20260530.md`
- Dirty files after write: same dirty artifact/code set, with this handoff
  updated.
- Disk after verification: `/dev/disk3s5   228Gi   153Gi    35Gi    82%    1.9M  364M    1%   /System/Volumes/Data`
- Input artifacts:
  - `docs/session_decision_record_20260530.md`
  - `docs/project_state.md`
  - `docs/decision_log.md`
  - `docs/artifact_index.md`
  - `docs/agent_runbook.md`
  - `work/selected_organic_cofactor_score_sidecars_current702_20260530.md`
  - `work/mechanism_relationship_eval_cofactor_augmented_current702_20260530.md`
  - `artifacts/v3_selected_organic_cofactor_score_sidecars_current702_20260530.json`
  - `artifacts/v3_sequence_cofactor_channel_current702_esm2_t30_150m_fallback_20260530.json`
  - `artifacts/v3_mechanism_relationship_eval_cofactor_augmented_current702_20260530.json`
  - `artifacts/v3_sequence_nn_label_manifest_current702_20260525.json`
  - `src/catalytic_earth/mechanism_relationship_eval.py`
  - `src/catalytic_earth/cli.py`
- Output artifacts:
  - `work/selected_organic_cofactor_score_sidecars_current702_20260530.md`
  - Automation memory updated for `catalytic-earth-work-loop`.
  - Existing selected sidecar and D11 artifacts were validated but not rewritten
    in this follow-up.
- Validation commands/results:
  - `python -m json.tool artifacts/v3_selected_organic_cofactor_score_sidecars_current702_20260530.json >/dev/null` passed.
  - `python -m json.tool artifacts/v3_sequence_cofactor_channel_current702_esm2_t30_150m_fallback_20260530.json >/dev/null` passed.
  - `python -m json.tool artifacts/v3_mechanism_relationship_eval_cofactor_augmented_current702_20260530.json >/dev/null` passed.
  - Corrected sidecar integrity probe passed: 2106 row-class records, 702
    non-null scores for each organic class, 0 unavailable rows, and exact
    current702 manifest entry match.
  - `PYTHONPATH=src python -m catalytic_earth.cli validate` passed: 12 source
    records, 8 mechanism fingerprints, 15 ontology families, 702 curated
    mechanism labels.
  - `PYTHONPATH=src python -m unittest tests.test_sequence_cofactor_channel tests.test_cofactor_channel_probe tests.test_predicted_geometry_robustness tests.test_cli`
    passed: 123 tests.
  - `PYTHONPATH=src python -m compileall -q src/catalytic_earth/mechanism_relationship_eval.py src/catalytic_earth/cli.py`
    passed.
  - `git diff --check` passed before this handoff update.
- Blockers:
  - Original selected t6/t12 row-level sidecars remain unrecovered.
  - Original full 2026-05-29 sequence cofactor channel JSON remains missing.
  - Strict reproduction of the original aggregate-selected organic cofactor
    channel remains blocked unless those inputs or cached weights are recovered.
- Exact next action: treat the ESM2-150M fallback sidecar plus cofactor-
  augmented D11 artifact as the current bounded pass, unless strict original
  t6/t12 reproduction is explicitly required.
- Next run should: `stop for this blocker` or `retarget` if a new gate is
  requested.

## Final Blocker Acceptance Verification

Run: `2026-05-31T00:56:03Z`

### Outcome

This run followed the latest handoff instead of restarting the search. The
latest relevant state already documented that the original selected t6/t12
sidecars and full 2026-05-29 channel JSON were unrecovered, that the
ESM2-150M fallback sidecar had non-null selected scores for all current702
rows, and that the cofactor-augmented D11 rerun had been executed.

I re-ran the bounded D11 writer and revalidated the artifacts. The D11 cofactor
sidecar blocker remains cleared at the documented fallback-source level:

- Selected sidecar row-class records: 2106.
- Non-null selected scores: flavin=702/702, heme=702/702, plp=702/702.
- `score_available=false`: 0.
- Unique selected entries: 702, exactly matching the current702 manifest.
- Selected source counts:
  `trained:esm2_t30_150m_existing_track` = 2106.
- Missingness flags: 60 row-class records still flagged
  `score_predicted_for_row_without_clean_experimental_cofactor_label`.
- Fallback channel predictions: 702 rows with 2106 non-null source-prefixed
  flavin/heme/plp class scores.
- D11 status: `real_d11_cofactor_augmented_rerun_complete`.
- Baseline predicted-score cosine family top3 any rate: 0.8.
- Cofactor-augmented predicted-score cosine family top3 any rate: 0.866667.
- Delta family top3 any rate: 0.066667.
- Non-tuning-adjacent augmented cosine family top3 any rate: 0.948718.
- Feature dimensions: 72 baseline, 78 cofactor-augmented.

No labels, registries, ontologies, imports, production scoring, global
thresholds, heldout splits, or model weights were changed in this run.

### Handoff

- Wall-clock start: `2026-05-30T19:56:03-0500`
- Wall-clock end: `2026-05-30T20:00:14-0500`
- Elapsed time: `4.20 minutes (252 seconds)`
- Git branch: `main`
- Git HEAD: `63fa60aceb1484539564fbe7081396777029d8da`
- Dirty files before write:
  - `M artifacts/v3_selected_organic_cofactor_score_sidecars_current702_20260530.json`
  - `M src/catalytic_earth/cli.py`
  - `M work/selected_organic_cofactor_score_sidecars_current702_20260530.md`
  - `?? artifacts/v3_mechanism_relationship_eval_cofactor_augmented_current702_20260530.json`
  - `?? artifacts/v3_sequence_cofactor_channel_current702_esm2_t30_150m_fallback_20260530.json`
  - `?? artifacts/v3_sequence_embedding_sidecar_current702_esm2_t12_35m_20260530_local_reacq_attempt.jsonl`
  - `?? artifacts/v3_sequence_embedding_sidecar_current702_esm2_t12_35m_20260530_local_reacq_attempt_summary.json`
  - `?? artifacts/v3_sequence_embedding_sidecar_current702_esm2_t30_150m_fallback_20260530.jsonl`
  - `?? artifacts/v3_sequence_embedding_sidecar_current702_esm2_t30_150m_fallback_20260530_summary.json`
  - `?? artifacts/v3_sequence_embedding_sidecar_current702_esm2_t6_8m_20260530_local_reacq_attempt.jsonl`
  - `?? artifacts/v3_sequence_embedding_sidecar_current702_esm2_t6_8m_20260530_local_reacq_attempt_summary.json`
  - `?? src/catalytic_earth/mechanism_relationship_eval.py`
  - `?? work/mechanism_relationship_eval_cofactor_augmented_current702_20260530.md`
- Dirty files after write: same dirty artifact/code set, with this handoff
  updated.
- Disk after verification:
  `/dev/disk3s5   228Gi   153Gi    35Gi    82%    1.9M  364M    1%   /System/Volumes/Data`
- Input artifacts:
  - `docs/session_decision_record_20260530.md`
  - `docs/project_state.md`
  - `docs/decision_log.md`
  - `docs/artifact_index.md`
  - `docs/agent_runbook.md`
  - `/Users/vivekvardhanarrabelli/.codex/automations/catalytic-earth-work-loop/memory.md`
  - `work/selected_organic_cofactor_score_sidecars_current702_20260530.md`
  - `work/mechanism_relationship_eval_cofactor_augmented_current702_20260530.md`
  - `artifacts/v3_selected_organic_cofactor_score_sidecars_current702_20260530.json`
  - `artifacts/v3_sequence_cofactor_channel_current702_esm2_t30_150m_fallback_20260530.json`
  - `artifacts/v3_mechanism_relationship_eval_cofactor_augmented_current702_20260530.json`
  - `artifacts/v3_sequence_nn_label_manifest_current702_20260525.json`
  - `src/catalytic_earth/mechanism_relationship_eval.py`
  - `src/catalytic_earth/cli.py`
- Output artifacts:
  - `artifacts/v3_mechanism_relationship_eval_cofactor_augmented_current702_20260530.json`
  - `work/mechanism_relationship_eval_cofactor_augmented_current702_20260530.md`
  - `work/selected_organic_cofactor_score_sidecars_current702_20260530.md`
  - `/Users/vivekvardhanarrabelli/.codex/automations/catalytic-earth-work-loop/memory.md`
- Validation commands/results:
  - `PYTHONPATH=src python -m catalytic_earth.cli build-mechanism-relationship-eval` passed and wrote the cofactor-augmented D11 artifact/report.
  - `python -m json.tool artifacts/v3_selected_organic_cofactor_score_sidecars_current702_20260530.json >/dev/null` passed.
  - `python -m json.tool artifacts/v3_sequence_cofactor_channel_current702_esm2_t30_150m_fallback_20260530.json >/dev/null` passed.
  - `python -m json.tool artifacts/v3_mechanism_relationship_eval_cofactor_augmented_current702_20260530.json >/dev/null` passed.
  - Corrected sidecar/channel/D11 integrity probe passed with the counts above.
    Two earlier ad hoc channel probes failed because they used stale schema keys
    (`rows`, then bare class names) before checking the current artifact schema.
  - `PYTHONPATH=src python -m catalytic_earth.cli validate` passed: 12 source
    records, 8 mechanism fingerprints, 15 ontology families, 702 curated
    mechanism labels.
  - `PYTHONPATH=src python -m unittest tests.test_sequence_cofactor_channel tests.test_cofactor_channel_probe tests.test_predicted_geometry_robustness tests.test_cli`
    passed: 123 tests.
  - `PYTHONPATH=src python -m compileall -q src/catalytic_earth/mechanism_relationship_eval.py src/catalytic_earth/cli.py`
    passed.
  - `git diff --check` passed.
- Blockers:
  - Original selected t6/t12 row-level sidecars remain unrecovered.
  - Original full 2026-05-29 sequence cofactor channel JSON remains missing.
  - Strict reproduction of the original aggregate-selected organic cofactor
    channel remains blocked unless those inputs or cached weights are recovered.
- Exact next action: stop this blocker thread and treat the ESM2-150M fallback
  sidecar plus cofactor-augmented D11 artifact as the current bounded pass;
  retarget only if strict original t6/t12 reproduction is explicitly required.
- Next run should: `stop for this blocker` or `retarget` to a new gate.
