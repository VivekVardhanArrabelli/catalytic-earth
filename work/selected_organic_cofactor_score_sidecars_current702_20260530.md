# Selected Organic Cofactor Score Sidecars current702

Run: 2026-05-30T18:56:28Z

## Decision

Blocked. I did not reconstruct or impute selected organic cofactor scores because the retained artifacts do not contain per-entry selected ESM scores, score bins, trained-head coefficients, or a full sequence cofactor channel JSON. Recomputing these scores would require recovering missing sidecars or rerunning/refitting the cofactor heads, which is outside this run scope.

No labels, registries, ontologies, imports, production scoring, thresholds, heldout splits, or model weights were changed. No model retraining or heldout tuning was performed.

## Output

- JSON blocker artifact: `artifacts/v3_selected_organic_cofactor_score_sidecars_current702_20260530.json`
- Row-class records: 2106 (702 current rows x 3 organic classes).
- Each row has `selected_score: null`, threshold metadata, selected source/model, source artifact path, missingness flags, and provenance hashes.

## Selected Sources

| Class | Selected source | Model | Aggregate AUC | Aggregate AP | Row-level status |
| --- | --- | --- | ---: | ---: | --- |
| flavin | trained:esm2_t12_35m | facebook/esm2_t12_35M_UR50D | 0.918622 | 0.732961 | blocked |
| heme | trained:esm2_t6_8m | facebook/esm2_t6_8M_UR50D | 0.866154 | 0.525794 | blocked |
| plp | trained:esm2_t6_8m | facebook/esm2_t6_8M_UR50D | 0.990956 | 0.876623 | blocked |

## Missing Inputs

| Required input | Observed status | Needed for |
| --- | --- | --- |
| `artifacts/v3_sequence_embedding_sidecar_current702_esm2_t12_35m_20260529.jsonl` | missing | flavin selected row-level scores |
| `artifacts/v3_sequence_embedding_sidecar_current702_esm2_t6_8m_20260529.jsonl` | present_empty_0_rows | heme selected row-level scores, plp selected row-level scores |
| `artifacts/v3_sequence_cofactor_channel_current702_20260529.json` | missing; only work/sequence_cofactor_channel_current702_20260529.md report is present | trained_sequence_heads.per_entry_scores, channel_predictions.scores |
| `trained cofactor head coefficients for esm2_t12_35m and esm2_t6_8m` | not persisted in committed artifacts | safe score recomputation without refitting |

## Checked But Insufficient

| Artifact | Why it cannot clear the blocker |
| --- | --- |
| `artifacts/v3_cofactor_channel_completion_summary_current702_20260529.json` | contains selected source aggregate metrics and confusion counts, not row-level scores or bins |
| `artifacts/v3_organic_cofactor_resolution_current702_20260530.json` | retains aggregate selected ESM metrics and k-mer nearest diagnostics, explicitly marks selected ESM row-level rows unavailable |
| `work/sequence_cofactor_channel_current702_20260529.md` | human report lists metrics and selected sources only, not per-entry scores |
| `artifacts/representation_tracks/esm2_150m/esm2_150m_embeddings_current702_20260525.jsonl` | different ESM2 150M model and mechanism classifier surface; using it for organic cofactor sidecars would require new head training and would not reproduce selected t6/t12 scores |

## Smallest Next Acquisition Job

Recover the original nonempty t6/t12 ESM JSONL sidecars plus artifacts/v3_sequence_cofactor_channel_current702_20260529.json from the runner/workspace that produced the summaries, then extract selected per-entry scores without refitting.

If recovery is unavailable, rerun the ESM sidecar acquisition with local cached weights only, then persist the full sequence cofactor channel JSON and extract selected per-entry scores. Candidate commands:

```bash
PYTHONPATH=src python -m catalytic_earth.cli build-sequence-embedding-sidecar --sequence-manifest artifacts/v3_sequence_manifest_current702_repaired_20260525.json --fasta artifacts/v3_sequence_distance_holdout_eval_current702_repaired_20260525.fasta --embedding-backend esm2_t6_8m_ur50d --model-name facebook/esm2_t6_8M_UR50D --local-files-only --no-fallback-to-largest-local-esm2 --out artifacts/v3_sequence_embedding_sidecar_current702_esm2_t6_8m_20260529.jsonl --summary artifacts/v3_sequence_embedding_sidecar_current702_esm2_t6_8m_20260529_summary.json
```

```bash
PYTHONPATH=src python -m catalytic_earth.cli build-sequence-embedding-sidecar --sequence-manifest artifacts/v3_sequence_manifest_current702_repaired_20260525.json --fasta artifacts/v3_sequence_distance_holdout_eval_current702_repaired_20260525.fasta --embedding-backend esm2_t12_35m_ur50d --model-name facebook/esm2_t12_35M_UR50D --local-files-only --no-fallback-to-largest-local-esm2 --out artifacts/v3_sequence_embedding_sidecar_current702_esm2_t12_35m_20260529.jsonl --summary artifacts/v3_sequence_embedding_sidecar_current702_esm2_t12_35m_20260529_summary.json
```

Then run a bounded score-persistence job that writes `artifacts/v3_sequence_cofactor_channel_current702_20260529.json` or a direct selected-score sidecar. Do not rerun D11 until flavin, heme, and PLP have non-null row-level selected scores for all 702 current rows.

## Validation Notes

- This artifact is intentionally a blocker artifact, not a pass artifact.
- Aggregate selected ESM metrics remain usable for context only; they are not row-level evidence.
- K-mer rows and ESM2 150M mechanism predictions were not substituted for selected t6/t12 cofactor scores.

## Required Handoff

- Wall-clock start: `2026-05-30T13:51:05-0500`
- Wall-clock end: `2026-05-30T13:58:00-0500`
- Elapsed time: `6.92 minutes (415 seconds)`
- Git branch: `main`
- Git HEAD: `a3a554ab49661a5a73ba1df4aa86f1ee9d031c1a`
- Dirty files before write: `clean`
- Dirty files after write:
  - `?? artifacts/v3_selected_organic_cofactor_score_sidecars_current702_20260530.json`
  - `?? work/selected_organic_cofactor_score_sidecars_current702_20260530.md`
- Disk after write: `/dev/disk3s5 228Gi 153Gi 35Gi 82% /System/Volumes/Data`
- Input artifacts:
  - `work/mechanism_relationship_eval_v0_20260530.md`
  - `artifacts/v3_mechanism_relationship_eval_v0_20260530.json`
  - `artifacts/v3_organic_cofactor_resolution_current702_20260530.json`
  - `work/organic_cofactor_resolution_current702_20260530.md`
  - `artifacts/v3_sequence_cofactor_channel_probe_current702_20260529.json`
  - `artifacts/v3_cofactor_channel_completion_summary_current702_20260529.json`
  - `work/sequence_cofactor_channel_current702_20260529.md`
  - `work/cofactor_channel_completion_summary_current702_20260529.md`
  - `artifacts/v3_sequence_embedding_sidecar_current702_esm2_t6_8m_20260529.jsonl`
  - `artifacts/v3_sequence_embedding_sidecar_current702_esm2_t6_8m_20260529_summary.json`
  - `artifacts/v3_sequence_embedding_sidecar_current702_esm2_t12_35m_20260529_summary.json`
  - `artifacts/v3_sequence_nn_label_manifest_current702_20260525.json`
  - `artifacts/representation_tracks/esm2_150m/esm2_150m_embeddings_current702_20260525.jsonl`
  - `artifacts/representation_tracks/esm2_150m/esm2_150m_predictions_current702_20260525.jsonl`
- Output artifacts:
  - `artifacts/v3_selected_organic_cofactor_score_sidecars_current702_20260530.json`
  - `work/selected_organic_cofactor_score_sidecars_current702_20260530.md`
- Validation commands/results:
  - `python -m json.tool artifacts/v3_selected_organic_cofactor_score_sidecars_current702_20260530.json` passed.
  - `PYTHONPATH=src python -m catalytic_earth.cli validate` passed: 12 source records, 8 mechanism fingerprints, 15 ontology families, 702 curated mechanism labels.
  - `git diff --check` passed.
  - Unit tests were not run because this was artifact/report-only and no code changed.
- Blockers: selected ESM row-level scores remain unavailable. The t6 JSONL exists but has 0 nonempty rows; the t12 JSONL is absent; `artifacts/v3_sequence_cofactor_channel_current702_20260529.json` is absent; trained cofactor-head coefficients were not persisted. Reconstructing scores would require recovering missing files or rerunning/refitting the cofactor heads, which this run was not authorized to do.
- Exact next action: recover the original nonempty t6/t12 ESM sidecars and full sequence cofactor channel JSON from the runner/workspace that produced the summaries. If recovery is impossible, explicitly authorize a bounded local-files-only sidecar reacquisition plus score-persistence job before rerunning D11.
- Next run should: `continue`.
