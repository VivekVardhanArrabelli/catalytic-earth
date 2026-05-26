# ESM-C Representation Track Handoff

Run timestamp: 2026-05-25T18:42:43Z
Standalone smoke artifact follow-up: 2026-05-26T02:14:29Z
Anomaly audit update: 2026-05-26T03:25:00Z

Branch: `research/representation-esm-c`

## 2026-05-26 Anomaly Audit Result

The suspicious ESM-C 300M cosine 1-NN result was reproduced exactly under the
original scoring head, but the embedding audit did not find corruption,
misalignment, truncation, or pooling breakage.

Current diagnosis:

- FASTA/index alignment is exact for all 760 repaired FASTA records.
- All 702 label-manifest rows map to exactly one first repaired sequence
  embedding; all 760 sequence records across multi-sequence entries are covered.
- The first repaired sequence per label row reproduces the original ESM-C
  heldout 1-NN predictions `140/140`.
- No NaN, inf, zero-norm, constant, or duplicate embedding rows were found.
- ESM-C tokenizer probe: `EsmSequenceTokenizer`, BOS `<cls>` id `0`, EOS
  `<eos>` id `2`, PAD id `1`, vocab size `33`.
- Longest repaired FASTA sequence had length `3011` and encoded to `3013`
  tokens, matching `sequence_length + BOS/EOS`; no truncation/windowing issue was
  observed.
- The main anomaly is scoring-head mismatch against the successful ESM-2 150M
  track: ESM-C was originally reported with cosine 1-NN, while ESM-2 150M used a
  train-split sklearn logistic probe on frozen embeddings.

New audit artifacts:

- `artifacts/representation_tracks/esm_c/esm_c_300m_embedding_sanity_audit_current702_20260526.json`
- SHA-256: `6c0ec7e8ea0d14dae5ca5c66dd0adb177c5ed94b4f2e6de92af574a8f630ad58`
- `artifacts/representation_tracks/esm_c/esm_c_300m_pipeline_comparison_to_esm2_current702_20260526.json`
- SHA-256: `1945f3e016014796131c991602c5c0503275bdfce674e65630a0297458f53f72`
- `artifacts/representation_tracks/esm_c/esm_c_300m_alternative_heads_current702_20260526.json`
- SHA-256: `a8c936db75534db6b405676fa65b913a715765797360caf3a060d689115eee67`

Corrected scoring-aligned artifacts, emitted separately without overwriting the
original 1-NN anomaly artifact:

- `artifacts/representation_tracks/esm_c/esm_c_300m_scoring_aligned_logistic_metrics_current702_20260526.json`
- SHA-256: `15244e29b7b19a8541a2099e103d69286495f6b4ed85508742903ffba66785d4`
- `artifacts/representation_tracks/esm_c/esm_c_300m_scoring_aligned_logistic_predictions_current702_20260526.jsonl`
- SHA-256: `80a53302658a27f7dfb70ee8609e4866da1be0d133e05ede984e884413805afd`

Corrected scoring-aligned ESM-C result:

- Head: frozen ESM-C embeddings plus train-split-only logistic regression with
  L2 normalization, train-fit standardization, `class_weight=balanced`, `C=1.0`.
- Heldout predictions: 140.
- Primary support: 45.
- Primary accuracy: `0.377778`.
- Primary macro-F1: `0.460220`.
- Exact label accuracy, all heldout rows: `0.671429`.
- OOS-label false-positive rate: `0.163043` (`15/92`).
- OOS-or-secondary false-positive rate: `0.168421` (`16/95`).

Comparison:

- Original ESM-C cosine 1-NN: primary accuracy `0.0889`, macro-F1 `0.1493`,
  OOS-label FP rate `0.3370`.
- Sequence-NN baseline: primary accuracy `0.1556`, OOS FP rate `0.2717`.
- ESM-2 150M reported logistic benchmark: primary accuracy `0.577778`,
  macro-F1 `0.695681`, OOS-or-secondary FP rate `0.168421`.
- Same-head ESM-2 cosine 1-NN diagnostic: primary accuracy `0.222222`,
  macro-F1 `0.367903`, OOS-or-secondary FP rate `0.221053`.

Conclusion: ESM-C 300M is not suspiciously broken under this setup after
scoring alignment, but it still underperforms ESM-2 150M logistic on primary
accuracy and macro-F1. No model-win claim should be made for ESM-C over ESM-2.

## Status

ESM-C 300M is unblocked and computed for the current702 representation track. No labels, fingerprints, ontology entries, production scoring, thresholds, or main docs were changed.

Track artifacts:

- `artifacts/representation_tracks/esm_c/esm_c_300m_backend_setup_current702_20260525.json`
- SHA-256: `66292518be6a680c6b7f230f512d52c739498096807a56659f0ffebe694527d6`
- `artifacts/representation_tracks/esm_c/esm_c_300m_smoke_embeddings_current702_20260525.json`
- SHA-256: `46f6d8f8529c31be70f176eda8f018cfc5cce1f5eb5bec04e95ee22eb9fb4f75`
- `artifacts/representation_tracks/esm_c/esm_c_300m_embeddings_manifest_current702_20260525.json`
- SHA-256: `8bf36bc4aaee58769c5a577b5dc1b5dae2acc1b5b136a261d18ef62624b03d7b`
- `artifacts/representation_tracks/esm_c/esm_c_300m_whole_sequence_embeddings_current702_20260525.npz`
- SHA-256: `29143be5fd8c034c5bfb8a3aa742ebb96c59e692de27234b152ac6fe456828a2`
- `artifacts/representation_tracks/esm_c/esm_c_300m_whole_sequence_embeddings_index_current702_20260525.jsonl`
- SHA-256: `c138a80886ee25f806a45dfc7850d8f885fbd1a29880459762565e343f2fce70`
- `artifacts/representation_tracks/esm_c/esm_c_300m_whole_sequence_cosine_nn_predictions_current702_20260525.jsonl`
- SHA-256: `ec704392b862d8e05674d05336f9878bae5ffe52dadcff534eca131af7d17498`
- `artifacts/representation_tracks/esm_c/esm_c_300m_whole_sequence_cosine_nn_metrics_current702_20260525.json`
- SHA-256: `b7cc6a2ae77e2bcc09bb21acb79d2ac10097889c0dd536e10caebc0f13fb295d`

Prior feasibility artifacts remain for audit trail:

- `artifacts/representation_tracks/esm_c/esm_c_feasibility_backend_blocker_current702_20260525.json`
- `artifacts/representation_tracks/esm_c/esm_c_bounded_backend_preflight_current702_20260525.json`

## Backend Setup

- Isolated runtime: `/private/tmp/esmc_runtime_20260525`.
- Package versions: `esm==3.2.3`, `torch==2.7.1`, `transformers==4.48.1`, `huggingface_hub==0.33.4`, `numpy==2.3.1`.
- Runtime size: 360,248,821 bytes. Pip cache: 102,310,229 bytes.
- Cache path: `/private/tmp/esm_c_hf_home_20260525`.
- Hugging Face cache apparent size after download: 3,996,517,080 bytes, including symlink-accounting and Xet transfer cache.
- Hugging Face hub cache apparent size after download/final cleanup: 2,664,197,181 bytes; disk usage is about 1.3 GB because the snapshot weight path is a symlink to the blob.
- Xet transient cache removed after download: 1,332,319,898 bytes; final Xet cache size: 0 bytes.
- Model requested: `EvolutionaryScale/esmc-300m-2024-12`.
- Model resolved: `biohub/esmc-300m-2024-12`.
- Checkpoint commit: `c309e1f43e775c1a513826dba9f1fe04622e96a1`.
- Weight file: `data/weights/esmc_300m_2024_12_v0.pth`.
- Weight size: 1,332,095,738 bytes.
- Weight SHA-256: `323dff9fbf3fef297a74f4f18b6528e6f2e599b0bcf72b6927516804015becea`.
- Metadata LFS blob id: `f86851ea1c05360f615c42d397d72ee3a2009e3a`.
- Device: CPU. ESM-C 6B and remote API were not used.
- Standalone two-record smoke artifact: `artifacts/representation_tracks/esm_c/esm_c_300m_smoke_embeddings_current702_20260525.json`.
- Smoke command used the existing isolated runtime/cache with `HF_HUB_OFFLINE=1` and `TRANSFORMERS_OFFLINE=1`; no remote API was used.
- Smoke result: 2 FASTA records, embedding dimension 960, model load 6.676 seconds, embedding forward 3.166 seconds.

## Metrics

Method: whole-sequence mean ESM-C embeddings excluding BOS/EOS, frozen cosine 1-NN over the repaired train/heldout split. No classifier was trained.

- Embedded FASTA records: 760.
- Total amino acids embedded: 318,251.
- Embedding dimension: 960.
- Batch count: 89.
- Total runtime: 971.089 seconds.
- Heldout predictions: 140.
- Primary supervised support: 45.
- Primary macro-F1: 0.1493.
- Primary accuracy: 0.0889.
- Exact label accuracy, all heldout rows: 0.4643.
- Exact label accuracy, in-scope heldout rows: 0.0833.
- OOS false-positive rate without threshold: 0.3370.
- OOS false-positive count: 31 of 92.
- Underpowered cells: 12 flagged, including `primary::heme_peroxidase_oxidase` with support 4.

Direct comparison recorded in the metrics artifact:

- Sequence-NN current702: primary macro-F1 0.2374, primary accuracy 0.1556, OOS FP rate 0.2717.
- Heuristic geometry current702: in-scope top1 accuracy 0.9792, OOS abstention rate 1.0, OOS false non-abstentions 0.
- 3Di smoke: no current702 artifact found in workspace.
- ProtT5: no current702 artifact found in workspace.
- ESM-2 150M: only an external-source review-only sample artifact was available, not a current702 full split metric.

## Contract State

- Pooling mode: `whole_sequence`; active-site pooling was not run.
- Predictive inputs: amino-acid sequence only.
- Forbidden predictive inputs used: none.
- Label registry edited: false.
- Fingerprint registry edited: false.
- Ontology registry edited: false.
- Production scoring changed: false.
- Large model training performed: false.
- Frozen classifier training performed: false.

## Verification

- Current anomaly-audit JSON artifacts validated with Python `json.load`.
- Corrected scoring-aligned prediction JSONL validated line-by-line with 140
  rows.
- `PYTHONPATH=src python -m catalytic_earth.cli validate` passed on the current
  run:
  - 12 source records
  - 8 mechanism fingerprints
  - 15 mechanism ontology families
  - 702 curated mechanism labels
- JSON artifacts validated with Python `json.load`.
- JSONL artifacts validated line-by-line: embeddings index has 760 rows; predictions has 140 rows.
- `PYTHONPATH=src python -m catalytic_earth.cli validate` passed:
  - 12 source records
  - 8 mechanism fingerprints
  - 15 mechanism ontology families
  - 702 curated mechanism labels
- Local commit created with commit-tree because the sandbox could not write the linked worktree index lock.
- Previous shell-git push blocker is cleared for the already-pushed ESM-C metric artifacts: at follow-up start, `git rev-parse HEAD` and `git rev-parse origin/research/representation-esm-c` both returned `63c8f0c72c9f36caf30c19b28be829b4289739f7`.
- Follow-up standalone smoke JSON artifacts validated with `json.load`; smoke NPZ loaded with shape `(2, 960)` and dtype `float32`; `PYTHONPATH=src python -m catalytic_earth.cli validate` re-run passed.
- Local branch commit for smoke artifacts: `7c77cf23bc95c702c666b1480598c2558f0d851d` (`Add ESM-C smoke artifacts`).
- HTTPS push remains blocked: `GIT_DIR=/Users/vivekvardhanarrabelli/Documents/Codex/2026-05-08/check-out-careflly-u-can-use-2/catalytic-earth/.git git push origin refs/heads/research/representation-esm-c:refs/heads/research/representation-esm-c` failed with `fatal: could not read Username for 'https://github.com': Device not configured`.
- SSH push fallback remains blocked: `GIT_DIR=/Users/vivekvardhanarrabelli/Documents/Codex/2026-05-08/check-out-careflly-u-can-use-2/catalytic-earth/.git git push git@github.com:VivekVardhanArrabelli/catalytic-earth.git refs/heads/research/representation-esm-c:refs/heads/research/representation-esm-c` failed with `git@github.com: Permission denied (publickey).`
- `gh auth status` reports the default GitHub token is invalid and suggests `gh auth login -h github.com`.
- GitHub connector lookup reached the repository but confirmed the local smoke commit is not present remotely: `_fetch_commit` for `7c77cf23bc95c702c666b1480598c2558f0d851d` returned `No commit found for SHA`.
- Required human action: restore GitHub shell credentials, then push local branch `research/representation-esm-c`.

## Next Exact Step

Review the new scoring-aligned ESM-C artifacts against the ESM-2 150M track.
The corrected ESM-C head clears the original anomaly versus sequence-NN but
still trails ESM-2 150M logistic; focus any model conclusion on that gap, not on
the stale 1-NN artifact alone.
