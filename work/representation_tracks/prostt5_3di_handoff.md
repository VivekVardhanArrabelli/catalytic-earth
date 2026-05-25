# ProstT5 / Foldseek 3Di Representation Track Handoff

Run date: 2026-05-25

## Scope

This track stayed on the frozen current702 sequence-hard split and did not reopen
the M-CSA `TM < 0.7` split-repair loop. No labels, fingerprints, ontology,
production scoring, thresholds, or shared artifact names were changed.

Predictive inputs used in the smoke baseline:

- Foldseek 3Di tokens derived from selected coordinate sidecars only.
- No EC labels, entry names, mechanism prose, expert notes, or production scores.
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

## Validation

Completed:

- `jq empty` on the new JSON artifacts.
- JSONL line-by-line `jq empty` on the new predictions artifact.
- `PYTHONPATH=src python -m catalytic_earth.cli validate`.

## Next Step

If this track continues, the next useful step is a bounded ProstT5 embedding
decision: either explicitly allow a bounded weights download/cache recording
step, or keep this as the Foldseek structure-derived 3Di token baseline and
compare it against the existing deterministic sequence-NN baseline only.
