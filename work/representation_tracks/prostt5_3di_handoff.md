# ProstT5 / Foldseek 3Di Representation Track Handoff

Run date: 2026-05-26

## Scope

This track stayed on the frozen current702 sequence-hard split and did not reopen
the M-CSA `TM < 0.7` split-repair loop. No labels, fingerprints, ontology,
production scoring, thresholds, or shared artifact names were changed.

Predictive inputs used in the smoke baseline:

- Foldseek 3Di tokens derived from selected coordinate sidecars only.
- No EC labels, entry names, mechanism prose, expert notes, source/review text,
  or production scores.
- Whole selected-structure pooling, implemented as the longest Foldseek 3Di
  record per selected PDB when Foldseek emitted multiple records.

## Feasibility

Primary artifact:
`artifacts/representation_tracks/prostt5_3di/current702_selected_structure_3di_feasibility_20260525.json`

3Di sidecar:
`artifacts/representation_tracks/prostt5_3di/current702_selected_structures_3di_20260525.fasta`

Findings:

- Foldseek is not on `PATH`, but an executable prior temp-env binary exists at
  `/private/tmp/catalytic-foldseek-env/bin/foldseek`.
- Foldseek version/hash recorded: `718d42176d2f67d36a60866fedfb881f8d5a7ebf`.
- Foldseek binary size recorded: `43024088` bytes.
- Structure-derived 3Di extraction works with:
  `createdb`, header DB link from `<db>_h` to `<db>_ss_h`, then
  `convert2fasta <db>_ss`.
- ProstT5 weights were not cached and were not downloaded. Installed Python
  dependencies are recorded in the feasibility artifact: torch `2.7.1`,
  transformers `4.53.2`, sentencepiece `0.2.0`.

Coverage:

- Current labels: 702.
- Selected PDB-backed rows: 696.
- Unique selected PDBs tokenized: 692.
- Tokenized label rows: 696 / 702.
- Heldout tokenized rows: 139 / 140.
- Untokenized rows: `m_csa:204`, `m_csa:372`, `m_csa:501`,
  `uniprot:P06744`, `uniprot:P78549`, `uniprot:Q3LXA3`.
- Only heldout untokenized row: `m_csa:372`, because it has
  `missing_selected_structure`.
- Cross-partition duplicate selected PDBs: 0.

## Smoke Result

Metrics artifact:
`artifacts/representation_tracks/prostt5_3di/current702_3di_nn_smoke_metrics_20260525.json`

Predictions artifact:
`artifacts/representation_tracks/prostt5_3di/current702_3di_nn_smoke_predictions_20260525.jsonl`

Model/tool id: `foldseek_3di_3mer_jaccard_nn.v1`

Training mode: no learned training; deterministic nearest-neighbor lookup over
whole selected-structure 3Di 3-mers under the frozen split.

Headline metrics:

- Heldout predictions: 139.
- Primary supervised accuracy: 0.1778.
- Primary macro-F1: 0.3133.
- Exact label accuracy, all heldout tokenized rows: 0.5899.
- Exact label accuracy, in-scope tokenized rows: 0.1702.
- OOS false-positive rate without threshold calibration: 0.1957.
- OOS abstention diagnostics by tier are included in the metrics artifact.
- Canary predictions and underpowered-cell flags are included.

Required provenance recorded in the artifacts:

- Eval contract SHA:
  `c4190f6f3f695185cd49e0de85d41280666c2986aaf2e359c8c4a60d67b40c50`.
- Sequence-NN metrics SHA:
  `22792684a943cd16987a73d048f801c3177a96c5967444d746a5aa768a0e6a26`.
- Split artifact SHA:
  `dbed4d1a60c09e97403f6be26ae52a3de49284ba35b6d6c2fb4efebb55de7425`.
- Sequence manifest SHA:
  `b792e03276e5027975c323fb65068804ca7a7a70fa388fdf33e71e98434aeb4b`.
- Coherence audit SHA:
  `cf9d5d3b17fa95d51374d244497ceba52414e60b8bdaefa12304ba3372cab734`.

## Wave 1 Standardized Export

Standardized predictions artifact:
`artifacts/representation_tracks/prostt5_3di/foldseek_3di_wave1_standardized_predictions_current702_20260526.jsonl`

Standardized metrics artifact:
`artifacts/representation_tracks/prostt5_3di/foldseek_3di_wave1_standardized_metrics_current702_20260526.json`

Schema:

- Prediction rows use `wave1_model_prediction_export.v1`.
- Metrics use `wave1_model_metrics_export.v1`.
- `model_track` is `foldseek_3di_token_nn`.
- `pooling_mode` is `whole_structure_3di_token_nn`.
- `active_site_pooling_contract` is `null`; no active-site pooling was used.

Row coverage:

- Standardized heldout rows: 140.
- Source tokenized 3Di NN predictions: 139.
- Explicit missing-coordinate/token blocker rows: 1, `m_csa:372`.
- Scope counts: 45 primary in-scope rows, 92 OOS rows, 3 secondary OOD probe
  rows.

Each standardized row carries branch/head commit, eval-contract and split
artifact SHAs, label/protein identifiers, true and predicted fingerprint state,
nearest-train score, primary-row correctness, OOS/secondary false-positive flag,
and missing-token blocker fields when applicable.

## 3Di vs Sequence-NN Readiness Comparison

Comparison artifact:
`artifacts/representation_tracks/prostt5_3di/current702_3di_vs_sequence_nn_readiness_20260525.json`

This artifact compares the Foldseek 3Di 3-mer NN smoke result against the
frozen deterministic sequence 3-mer NN baseline on the same repaired split.
It does not download or run ProstT5 weights.

Main deltas, reported as 3Di minus sequence-NN:

- Prediction count: `-1`, because held-out `m_csa:372` lacks a tokenized
  selected structure.
- Primary supervised accuracy: `+0.0222`.
- Recomputed primary macro-F1: `+0.0759`.
- Exact label accuracy across all held-out predictions: `+0.0613`.
- Exact label accuracy on in-scope held-out rows: `+0.0244`.
- OOS false-positive rate without threshold calibration: `-0.0760`.

Row-level overlap:

- Common held-out predictions: 139.
- Common primary supervised rows: 45.
- Both baselines top-1 correct on 3 primary rows.
- 3Di-only top-1 correct on 5 primary rows.
- Sequence-only top-1 correct on 4 primary rows.
- Neither top-1 correct on 33 primary rows.

OOS diagnostics:

- Far-OOS false-positive rate moved from `1.0000` to `0.0000`, but this is a
  single row.
- Near-OOS false-positive rate was unchanged at `0.3333`.
- Unknown-OOS false-positive rate moved from `0.2614` to `0.1932`.
- Canary changes are explicitly listed; `m_csa:372` remains a missing-structure
  3Di canary case, while 3Di abstains on `m_csa:853` where sequence-NN does not.

Decision:

- Foldseek 3Di tokens are ready as a bounded, track-local structure-alphabet
  baseline for review.
- ProstT5 remains blocked for this run. The canonical `Rostlab/ProstT5` repo
  has an 11,275,478,387 byte `pytorch_model.bin`; `Rostlab/ProstT5_fp16` has a
  5,637,876,077 byte `pytorch_model.bin`. Neither snapshot is cached under the
  probed Hugging Face cache paths, and this runtime has no CUDA or MPS backend,
  so embedding would be CPU-only after a large uncached download.
- No learned superiority claim is made; underpowered fingerprint/diversity cells
  remain descriptive only.

## ProstT5 Backend Setup Blocker

Backend setup artifact:
`artifacts/representation_tracks/prostt5_3di/current702_prostt5_backend_setup_terminal_blocker_20260525.json`

The bounded backend decision is terminal for this run:

- Probed cache paths:
  `/Users/vivekvardhanarrabelli/.cache/huggingface/hub` and
  `/private/tmp/catalytic-earth-hf-cache/hub`.
- Local-only `snapshot_download` probes failed with `LocalEntryNotFoundError`
  for both `Rostlab/ProstT5` and `Rostlab/ProstT5_fp16`.
- Tool versions recorded: torch `2.7.1`, transformers `4.53.2`,
  sentencepiece `0.2.0`, huggingface_hub `0.33.4`; `accelerate` is missing.
- Accelerator probe recorded: CUDA unavailable, MPS built but unavailable.
- Existing ESM-2 150M cache context was observed under
  `/private/tmp/catalytic-earth-hf-cache`, but there is no current702
  frozen-split ESM-2 150M or ProtT5 comparator artifact for this track.
- No ProstT5 embeddings manifest, predictions JSONL, or metrics JSON were
  emitted because the backend is unavailable locally.

## Final ProstT5 Backend Preflight

Final preflight artifact:
`artifacts/representation_tracks/prostt5_3di/current702_prostt5_final_backend_preflight_20260525.json`

The final bounded preflight used local-only cache checks and did not download
model weights:

- `Rostlab/ProstT5_fp16` is not cached under
  `/Users/vivekvardhanarrabelli/.cache/huggingface/hub` or
  `/private/tmp/catalytic-earth-hf-cache/hub`.
- `Rostlab/ProstT5` is also not cached under either probed path.
- Accelerator probe: CUDA unavailable; MPS built but unavailable; selected
  backend would be CPU if weights appeared later.
- Two-record ProstT5 smoke was not run. The smoke gate required cached fp16
  weights or an accelerator; neither condition was met.
- Terminal blocker is retained. Unblocking still needs explicit multi-GB weight
  download approval plus an accelerator-capable runtime or accepted CPU smoke
  window.

Current ProstT5 full-model blocker artifact:
`artifacts/representation_tracks/prostt5_3di/prostt5_full_model_blocker_current702_20260526.json`

The current blocker keeps the same terminal decision with a fresh local
filesystem cache scan:

- No canonical or fp16 ProstT5 snapshot/weight file is present under the probed
  Hugging Face cache roots.
- CUDA is unavailable and MPS is built but unavailable; a later run would select
  CPU unless the runtime changes.
- No ProstT5 embeddings, predictions, or metrics were emitted.
- Unblocking still requires explicit multi-GB weight download approval plus an
  accelerator-capable runtime or accepted CPU embedding window.

Comparator rollup artifact:
`artifacts/representation_tracks/prostt5_3di/current702_3di_comparator_rollup_20260525.json`

Comparator scan:

- Direct current702 comparators found locally: Foldseek 3Di token NN and
  deterministic sequence-NN.
- Foldseek 3Di token NN: 139 heldout predictions, primary supervised accuracy
  `0.1778`, macro-F1 `0.3133`, exact label accuracy all `0.5899`, OOS
  false-positive rate `0.1957`.
- Sequence-NN: 140 heldout predictions, primary supervised accuracy `0.1556`,
  macro-F1 `0.2374`, exact label accuracy all `0.5286`, OOS false-positive
  rate `0.2717`.
- 3Di minus sequence-NN: primary supervised accuracy `+0.0222`, macro-F1
  `+0.0759`, exact label accuracy all `+0.0613`, OOS false-positive rate
  `-0.0760`.
- No local current702 frozen-split metrics or predictions were found for ESM-2,
  ESM-C, ProtT5, SaProt, or a separate Foldseek structural-NN comparator. Local
  ESM-2 references are prior external/control context, and local Foldseek/TM
  artifacts are coordinate-readiness or split/leakage screens, not direct
  current702 representation comparators.

## Validation

Completed:

- `jq empty` on
  `foldseek_3di_wave1_standardized_metrics_current702_20260526.json`,
  `prostt5_full_model_blocker_current702_20260526.json`, the final preflight,
  and comparator rollup artifacts.
- JSONL line-by-line `jq -c .` on
  `foldseek_3di_wave1_standardized_predictions_current702_20260526.jsonl`
  reported 140 valid rows.
- Python JSON assertions confirmed 140 standardized heldout rows, 139 tokenized
  predictions, and one missing-token blocker row.
- `PYTHONPATH=src python -m catalytic_earth.cli validate`.
- `python -m json.tool` on the standardized metrics and current ProstT5 blocker
  artifacts.

## Next Step

This run keeps the Foldseek structure-derived 3Di token baseline as the completed
structural-alphabet result. A future ProstT5 embedding run needs explicit large
cache approval plus either an accelerator-capable runtime or an accepted long CPU
embedding window.
