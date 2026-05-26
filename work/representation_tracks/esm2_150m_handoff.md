# ESM-2 150M representation track handoff

Run timestamp: 2026-05-25T16:23:44Z

## Scope

This branch ran the Catalytic Earth representation benchmark track for `facebook/esm2_t30_150M_UR50D` only.

The benchmark used whole-sequence amino-acid inputs from the repaired current702 sequence FASTA and split assignment. It did not use EC labels, entry names, mechanism prose, expert notes, curator rationale text, review decision text, or source identifiers as predictive features. No labels, fingerprints, ontology files, production scoring, or thresholds were edited.

## Frozen lineage

- Baseline branch/commit: `origin/main` at `8e69bf002097d5cf55521a13764e096908d8e0af`
- Eval contract: `artifacts/v3_mechanism_prediction_oos_and_diversity_eval_contract_702.json`
- Eval contract SHA256: `c4190f6f3f695185cd49e0de85d41280666c2986aaf2e359c8c4a60d67b40c50`
- Fingerprint audit: `artifacts/v3_mechanism_fingerprint_v1_coherence_audit_702.json`
- Sequence manifest: `artifacts/v3_sequence_manifest_current702_repaired_20260525.json`
- Sequence manifest SHA256: `b792e03276e5027975c323fb65068804ca7a7a70fa388fdf33e71e98434aeb4b`
- Split artifact: `artifacts/v3_sequence_distance_holdout_eval_1025_current702_split_assignment_repaired_20260525.json`
- Split artifact SHA256: `dbed4d1a60c09e97403f6be26ae52a3de49284ba35b6d6c2fb4efebb55de7425`
- Sequence-NN metrics: `artifacts/v3_sequence_nn_metrics_current702_20260525.json`
- Sequence-NN metrics SHA256: `22792684a943cd16987a73d048f801c3177a96c5967444d746a5aa768a0e6a26`

## Artifacts

- `artifacts/representation_tracks/esm2_150m/esm2_150m_backend_execution_current702_20260525.json`
- `artifacts/representation_tracks/esm2_150m/esm2_150m_embeddings_manifest_current702_20260525.json`
- `artifacts/representation_tracks/esm2_150m/esm2_150m_embeddings_current702_20260525.jsonl`
- `artifacts/representation_tracks/esm2_150m/esm2_150m_predictions_current702_20260525.jsonl`
- `artifacts/representation_tracks/esm2_150m/esm2_150m_metrics_current702_20260525.json`
- `artifacts/representation_tracks/esm2_150m/esm2_150m_lineage_verification_current702_20260526.json`

Output SHA256 values are recorded in the backend execution artifact.

## Backend and pooling

- Model id: `facebook/esm2_t30_150M_UR50D`
- Backend status: computed
- Device: CPU
- Runtime: 751.05 seconds
- Embedding dim: 640
- Pooling mode: `whole_sequence`
- Pooling method: mean of last hidden-state residue tokens across the full sequence.
- Long-sequence handling: sequences above the ESM positional limit were split into non-overlapping windows of up to 1022 residues, then residue-count-weighted back into one whole-sequence embedding.
- Default Hugging Face cache blocker: `~/.cache/huggingface` was not writable. The run used `HF_HOME=/private/tmp/catalytic-earth-hf-cache`.

## Results

Primary heldout metrics:

- Primary macro-F1: `0.695681`
- Primary accuracy: `0.577778`
- Primary support count: `45`
- Exact label accuracy across all heldout rows: `0.735714`

Sequence-NN baseline comparison:

- Sequence-NN primary accuracy: `0.1556`
- Sequence-NN OOS false-positive rate without threshold: `0.2717`

Per-fingerprint heldout accuracy:

- `ser_his_acid_hydrolase`: `0.75` on 8 rows
- `metal_dependent_hydrolase`: `0.588235` on 17 rows
- `plp_dependent_enzyme`: `0.833333` on 6 rows
- `flavin_dehydrogenase_reductase`: `0.4` on 10 rows
- `heme_peroxidase_oxidase`: `0.25` on 4 rows, underpowered for macro-F1

OOS diagnostics:

- OOS/secondary-probe heldout count: `95`
- OOS false-positive non-abstention rate: `0.168421`
- Boundary OOS: 1 row, 0 false-positive non-abstentions, underpowered
- Far OOS: 2 rows, 0 false-positive non-abstentions, underpowered
- Near OOS: 4 rows, 2 false-positive non-abstentions, underpowered
- Unknown OOS: 88 rows, 14 false-positive non-abstentions

## Limitations

- The classifier is a small sklearn logistic regression trained on frozen ESM-2 embeddings from the in-distribution split; this is not large-model training.
- Abstention is only the learned `out_of_scope` class. No heldout-tuned confidence threshold was selected.
- The eval contract only freezes representative OOS tiers. Unassigned out-of-scope heldout rows are reported as `unknown_oos` pending a full per-entry OOS tier artifact.
- All per-fingerprint accuracy/recall cells are qualitative under the contract's 30-row threshold, and all diversity-bin cells are qualitative under the same threshold.
- This is a representation baseline, not a validated enzyme-function claim.

## Verification

Passed:

```bash
jq -e . artifacts/representation_tracks/esm2_150m/esm2_150m_backend_execution_current702_20260525.json artifacts/representation_tracks/esm2_150m/esm2_150m_embeddings_manifest_current702_20260525.json artifacts/representation_tracks/esm2_150m/esm2_150m_metrics_current702_20260525.json >/dev/null
jq -c . artifacts/representation_tracks/esm2_150m/esm2_150m_embeddings_current702_20260525.jsonl >/dev/null
jq -c . artifacts/representation_tracks/esm2_150m/esm2_150m_predictions_current702_20260525.jsonl >/dev/null
PYTHONPATH=src python -m catalytic_earth.cli validate
PYTHONPATH=src python -m unittest tests.test_representation_baseline
```

Focused jq lineage checks also passed for model id, pooling mode, no forbidden inputs, eval contract SHA, sequence-NN metrics SHA, split artifact, and OOS diagnostics status.

Validation refresh:

- Run timestamp: `2026-05-25T18:15:50Z`
- Added validation artifact: `artifacts/representation_tracks/esm2_150m/esm2_150m_validation_current702_20260525_run2.json`
- Re-checked JSON/JSONL parse validity, backend-recorded output hashes, ESM-2 150M lineage fields, required metrics fields, canary rows, underpowered-cell flags, `PYTHONPATH=src python -m unittest tests.test_representation_baseline`, and `PYTHONPATH=src python -m catalytic_earth.cli validate`.
- This refresh did not regenerate embeddings or predictions and did not mix active-site pooling into the whole-sequence evidence budget.

Lineage verification refresh:

- Run timestamp: `2026-05-26T02:07:49Z`
- Added lineage verification artifact: `artifacts/representation_tracks/esm2_150m/esm2_150m_lineage_verification_current702_20260526.json`
- Re-confirmed branch and remote were at `6bc960d9fcabb7d58835ca6082b26c66567d0f75` before this audit, with `origin/main` at the frozen baseline `8e69bf002097d5cf55521a13764e096908d8e0af`.
- Re-cited the eval contract SHA, sequence-NN metrics SHA, split artifact SHA, model id, whole-sequence pooling mode, amino-acid-only leakage contract, OOS abstention diagnostics, canary count, and underpowered-cell status in a compact track-scoped artifact.
- Passed JSON/JSONL parsing, focused jq lineage assertions, `PYTHONPATH=src python -m unittest tests.test_representation_baseline`, and `PYTHONPATH=src python -m catalytic_earth.cli validate`.
- This audit did not regenerate embeddings or predictions and did not mix active-site pooling into the whole-sequence evidence budget.
