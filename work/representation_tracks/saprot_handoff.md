# SaProt Representation Track Handoff

Run date: 2026-05-25
Branch: research/representation-saprot

## Artifact

- `artifacts/representation_tracks/saprot/saprot_feasibility_current702_20260525.json`

## Decision

Do not run full SaProt embeddings yet. The current sequence split is ready, and a bounded Foldseek 3Di conversion smoke passed on one staged selected PDB, but the full backend is not clean enough for a current702 SaProt result.

## Required citations recorded

- Eval contract: `artifacts/v3_mechanism_prediction_oos_and_diversity_eval_contract_702.json`, SHA256 `c4190f6f3f695185cd49e0de85d41280666c2986aaf2e359c8c4a60d67b40c50`
- Sequence-NN metrics: `artifacts/v3_sequence_nn_metrics_current702_20260525.json`, SHA256 `22792684a943cd16987a73d048f801c3177a96c5967444d746a5aa768a0e6a26`
- Split artifact: `artifacts/v3_sequence_distance_holdout_eval_1025_current702_split_assignment_repaired_20260525.json`, SHA256 `dbed4d1a60c09e97403f6be26ae52a3de49284ba35b6d6c2fb4efebb55de7425`
- Model id: `westlake-repl/SaProt_650M_AF2_candidate_not_downloaded`
- Pooling mode: `whole_sequence`
- Structure source: selected PDB local mmCIF from current702 split and geometry features
- Input leakage contract: amino-acid sequence plus structure-derived 3Di tokens only; no EC/name/prose/expert-note/source-id predictive features
- OOS diagnostics: not computed for SaProt because backend is blocked; sequence-NN OOS diagnostics are cited as comparator context

## Coverage Findings

- Sequence coverage is complete for current702: 702 of 702 labels, with 2 selected-PDB sequence fallbacks.
- Frozen split is 562 in-distribution and 140 held out; max observed train/test sequence identity is 0.284.
- Selected PDB coverage is partial: 696 rows have selected PDB keys, 676 rows have local selected-PDB coordinates, and 26 rows are blocked.
- Blocked rows are 20 in-distribution and 6 held out.
- Reference structure crossrefs include AFDB for 680 rows and PDB for 693 rows, but the current selected-structure path is PDB/mmCIF; no AFDB coordinate cache was staged for SaProt in this run.

## Backend Findings

- Foldseek is available only at `/private/tmp/catalytic-foldseek-env/bin/foldseek`, not on `PATH`; version output was `718d42176d2f67d36a60866fedfb881f8d5a7ebf`.
- A bounded 3Di smoke on `artifacts/v3_foldseek_coordinates_1000/pdb_1B73.cif` completed with matched AA and 3Di token lengths, 252 and 252.
- `torch` 2.7.1 and `transformers` 4.53.2 are installed.
- `saprot` and `esm` Python packages are not installed.
- Hugging Face and torch cache paths do not exist; no model was downloaded, so model size was not recorded.

## Next Step

Freeze the exact SaProt model/cache policy and chain-alignment policy, then materialize or formally exclude the 26 rows missing selected local coordinates before attempting even a bounded embedding smoke.
