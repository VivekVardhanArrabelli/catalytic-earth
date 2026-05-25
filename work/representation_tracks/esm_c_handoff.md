# ESM-C Representation Track Handoff

Run timestamp: 2026-05-25T18:42:43Z

Branch: `research/representation-esm-c`

## Status

ESM-C 300M is unblocked and computed for the current702 representation track. No labels, fingerprints, ontology entries, production scoring, thresholds, or main docs were changed.

Track artifacts:

- `artifacts/representation_tracks/esm_c/esm_c_300m_backend_setup_current702_20260525.json`
- SHA-256: `66292518be6a680c6b7f230f512d52c739498096807a56659f0ffebe694527d6`
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

- JSON artifacts validated with Python `json.load`.
- JSONL artifacts validated line-by-line: embeddings index has 760 rows; predictions has 140 rows.
- `PYTHONPATH=src python -m catalytic_earth.cli validate` passed:
  - 12 source records
  - 8 mechanism fingerprints
  - 15 mechanism ontology families
  - 702 curated mechanism labels

## Next Exact Step

Review the ESM-C metrics against the sequence-NN and geometry baselines. ESM-C 300M is worse than sequence-NN on primary macro-F1, primary accuracy, and OOS false-positive rate in this frozen 1-NN setup, so no win claim should be made from this run.
