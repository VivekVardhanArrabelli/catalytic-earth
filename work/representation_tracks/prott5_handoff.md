# ProtT5 Representation Track Handoff

Run dates: artifact generation 2026-05-25; verification refresh 2026-05-26T02:16:17Z (2026-05-25 CDT)
Branch: `research/representation-prott5`

## Output

- Metrics artifact: `artifacts/representation_tracks/prott5/prott5_current702_swissprot_h5_knn_metrics_20260525.json`
  SHA-256 `f37c3aa780c6d2ec169f36ee38a02fdcd4dee957a54483972bb2e54000d61959`
- Predictions artifact: `artifacts/representation_tracks/prott5/prott5_current702_swissprot_h5_knn_predictions_20260525.jsonl`
- H5 key coverage artifact: `artifacts/representation_tracks/prott5/prott5_current702_swissprot_h5_key_coverage_20260525.json`
- Prior feasibility/blocker artifact, now superseded by exact H5 probing: `artifacts/representation_tracks/prott5/prott5_current702_swissprot_embedding_feasibility_20260525.json`

## Coverage

- Exact H5 coverage: 666 / 702 current rows have at least one UniProtKB/Swiss-Prot ProtT5 per-protein embedding.
- Heldout prediction coverage: 132 / 140 heldout rows.
- Train coverage: 534 / 562 in-distribution rows.
- Referenced current702 accessions: 760 total; 721 present in the H5, 39 missing.
- Real sequence accessions in the repaired split: 758 total; 721 present in the H5, 37 missing.
- Missing heldout rows: `m_csa:67`, `m_csa:201`, `m_csa:372`, `m_csa:428`, `m_csa:453`, `m_csa:509`, `m_csa:634`, `m_csa:688`.
- Missing heldout accessions: `O52942`, `Q9X4K7`, `Q712I6`, `Q9ZF13`, `O68884`, `Q9X592`, `P84147`, `Q5JP69`.

## Model and Pooling Contract

- Model/source id: UniProtKB/Swiss-Prot embeddings `uniprot_sprot/per-protein.h5`, ProtT5/prottrans_t5_xl_u50 source vectors.
- Local H5 size: 1,383,407,848 bytes; SHA-256 `15d7bc28aca161e70e25bd7ad51bc49a9824677e9cb28cbdd69765d0029d62d5`; 574,615 top-level accession-keyed vectors; 1024-dimensional `float16`.
- Pooling mode: whole-sequence per-protein vectors only. Rows with multiple available accessions use mean pooling over L2-normalized accession vectors, followed by row L2 normalization.
- kNN mode: cosine 1-nearest-neighbor against frozen in-distribution split rows; no trained probe and no large-model training.
- Abstention policy: abstain only when the nearest train row label group is `out_of_scope`; no similarity threshold was selected.
- Active-site pooling was not attempted and remains reserved for a separate `known_active_site_window_ablation`.
- Input leakage contract: only ProtT5 embedding vectors are predictive inputs. No EC labels, entry names, mechanism prose, expert notes, Rhea/source prose, review decisions, production scores, labels, ontology, or thresholds were edited or used as predictive features.

## Metrics

- Primary supervised accuracy: 0.3953 on 43 embedded primary heldout rows.
- Primary macro-F1: 0.5759.
- Exact label accuracy across embedded heldout rows: 0.6364 on 132 predictions.
- OOS primary false-positive/non-abstention rate: 0.2299 on 87 embedded out-of-scope heldout rows.
- OOS abstention rate: 0.7701.
- Sequence-NN comparison from the frozen baseline: primary accuracy improved from 0.1556 to 0.3953; OOS false-positive rate improved from 0.2717 to 0.2299, with the caveat that ProtT5 covers 132/140 heldout rows because Swiss-Prot H5 lacks TrEMBL/fallback entries.
- ESM-2 150M comparator from local branch `research/representation-esm2-150m` (`6bc960d`): primary accuracy 0.577778, macro-F1 0.695681, OOS false-positive/non-abstention rate 0.168421 on 140/140 heldout rows. ProtT5 is lower by 0.182478 accuracy and 0.119781 macro-F1, and higher by 0.061479 OOS false-positive rate; this comparison mixes representation, model head, and coverage differences.

Underpowered cells are flagged in the artifact at top-level `underpowered_cell_flags` and inside the detailed breakdowns. The heme heldout cell has only 4 embedded rows and remains qualitative under the contract's macro-F1 class minimum; the `boundary_oos` embedded out-of-scope tier has 0 rows; the radical-SAM secondary canary `m_csa:372` is missing from the H5.

## Required Citations

- Eval contract: `artifacts/v3_mechanism_prediction_oos_and_diversity_eval_contract_702.json`
  SHA-256 `c4190f6f3f695185cd49e0de85d41280666c2986aaf2e359c8c4a60d67b40c50`
- Sequence-NN baseline: `artifacts/v3_sequence_nn_metrics_current702_20260525.json`
  SHA-256 `22792684a943cd16987a73d048f801c3177a96c5967444d746a5aa768a0e6a26`
- Split artifact: `artifacts/v3_sequence_distance_holdout_eval_1025_current702_split_assignment_repaired_20260525.json`
  SHA-256 `dbed4d1a60c09e97403f6be26ae52a3de49284ba35b6d6c2fb4efebb55de7425`
- Sequence manifest: `artifacts/v3_sequence_manifest_current702_repaired_20260525.json`
  SHA-256 `b792e03276e5027975c323fb65068804ca7a7a70fa388fdf33e71e98434aeb4b`
- Fingerprint audit: `artifacts/v3_mechanism_fingerprint_v1_coherence_audit_702.json`
  SHA-256 `cf9d5d3b17fa95d51374d244497ceba52414e60b8bdaefa12304ba3372cab734`
- H5 key coverage artifact: `artifacts/representation_tracks/prott5/prott5_current702_swissprot_h5_key_coverage_20260525.json`
  SHA-256 `4c90d425f124ec7fabe56bc6864f95c0462472c7164b4f7b6b6e8bff0fed81dc`
- ESM-2 150M comparator metrics: `research/representation-esm2-150m:artifacts/representation_tracks/esm2_150m/esm2_150m_metrics_current702_20260525.json`
  SHA-256 `b67dee9010e5dc0c20c92709fe6094b29228d07b151c9fcbe1d11530edc7fa6b`

## Verification

- Fresh H5 probe on 2026-05-26T02:13:44Z opened `artifacts/representation_tracks/prott5/downloads/uniprot_sprot_per-protein.h5` with `h5py`; size is 1,383,407,848 bytes, SHA-256 is `15d7bc28aca161e70e25bd7ad51bc49a9824677e9cb28cbdd69765d0029d62d5`, top-level key count is 574,615, and sample dataset `A0A009IHW8` is shape `[1024]` dtype `float16`.
- `jq -e` validation passed for the metrics artifact.
- `jq -e` validation passed for the H5 key coverage artifact.
- JSONL parsing validation passed for 132 prediction rows.
- `PYTHONPATH=src python -m catalytic_earth.cli validate` passed.
- Local branch contains the metrics and handoff refresh commits, but push is blocked in this environment: `git push origin HEAD:refs/heads/research/representation-prott5` fails with `fatal: could not read Username for 'https://github.com': Device not configured`; `gh auth status` reports an invalid token. Direct remote check still reports `origin/research/representation-prott5` at `fceaadb4a5b6d538e22bacfc318c63a810cef882`.

## Next Step

Authenticate push access, then push local `research/representation-prott5` HEAD. After that, review the missing-H5 heldout rows before interpreting the win claim broadly. The main unresolved risk is coverage bias from Swiss-Prot-only vectors, especially the missing radical-SAM secondary probe `m_csa:372` and two missing `ser_his_acid_hydrolase` primary rows.
