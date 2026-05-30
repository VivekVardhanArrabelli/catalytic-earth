# SaProt Representation Track Handoff

Run date: 2026-05-25
Branch: research/representation-saprot

## 2026-05-26 Wave 1 Standardized Export

Standardized SaProt row-level audit artifacts were emitted from the cached
bounded SaProt-35M heldout predictions only. No new SaProt setup, model
download, active-site pooling, registry edit, threshold edit, or label edit was
performed.

New Wave 1 artifacts:

- `artifacts/representation_tracks/saprot/saprot_wave1_standardized_predictions_current702_20260526.jsonl`
- `artifacts/representation_tracks/saprot/saprot_wave1_standardized_metrics_current702_20260526.json`
- `artifacts/representation_tracks/saprot/saprot_wave1_standardized_blocker_or_coverage_current702_20260526.json`

The prediction export contains 140 heldout rows: 45 primary in-scope rows, 92
out-of-scope rows, and 3 secondary-probe rows. All rows use
`schema_version=wave1_model_prediction_export.v1`, `model_track=saprot`, and
`pooling_mode=whole_structure_sequence`; `active_site_pooling_contract` is
`null` throughout. The row schema carries backend/model identity, frozen
selected-structure and Foldseek chain policy provenance, branch/head commit,
eval contract and split hashes, row/label/M-CSA/protein identifiers, true and
predicted fingerprint fields, confidence scores, primary correctness, OOS or
secondary false-positive flags, abstention flags, missing-coordinate flags, and
chain/token blockers where applicable.

The standardized metrics preserve the cached SaProt headline result:

- Primary macro-F1: 0.5134
- Primary supervised accuracy: 0.3333, 15/45
- Embedded heldout rows: 133
- Heldout coordinate/tokenization abstentions: 7
- OOS false-positive rate without threshold: 0.1957, 18/92

Full current702 prediction rows are not locally available. The blocker/coverage
artifact records this explicitly: the cached prediction artifact covers heldout
rows only, while 562 in-distribution rows remain train/lookup references under
the frozen split. Structure-token coverage remains 661/702 ready for SaProt
embedding and 41/702 blocked before embedding, including 7 heldout blockers.
Blocked reasons are 20 unstaged selected PDB coordinates, 9 unsupported Foldseek
AA-token rows, 6 over-length selected records, 4 non-PDB/unrecognized selected
structure proxies, and 2 missing selected-structure proxies.

Comparator status in the standardized metrics:

- Sequence-NN current702 comparator is available directly.
- Foldseek local artifacts are available as tokenization coverage and a
  non-predictive TM-score signal; no Foldseek classifier metric is mixed with
  SaProt metrics.
- ESM-2 artifacts are available only as external-source review-only samples,
  not as current702 direct metrics.
- ProtT5 and ESM-C current702 metrics were not found locally.

## Decision

SaProt is no longer blocked at generic feasibility. A bounded public HF/Transformers SaProt-35M run was completed on the frozen current702 split using whole selected-structure Foldseek SA tokens and nearest-neighbor lookup over in-distribution embeddings.

This is not a full SaProt-650M result. The 650M repository was metadata-checked only and not downloaded because the public repo reports about 5.21 GB across duplicate `.pt` and `pytorch_model.bin` weight formats.

## New Artifacts

- `artifacts/representation_tracks/saprot/saprot_chain_token_policy_current702_20260525.json`
- `artifacts/representation_tracks/saprot/saprot_tokenization_coverage_current702_20260525.json`
- `artifacts/representation_tracks/saprot/saprot_sa_tokens_current702_20260525.jsonl`
- `artifacts/representation_tracks/saprot/saprot_embeddings_manifest_current702_20260525.json`
- `artifacts/representation_tracks/saprot/saprot_predictions_current702_20260525.jsonl`
- `artifacts/representation_tracks/saprot/saprot_metrics_current702_20260525.json`

Prior feasibility artifact retained:

- `artifacts/representation_tracks/saprot/saprot_feasibility_current702_20260525.json`

## Frozen Chain/Token Policy

- Use the selected structure provenance from the frozen current702 split artifact.
- For each selected coordinate, parse all Foldseek `structureto3didescriptor` records.
- If multiple records are emitted, choose the longest amino-acid/3Di record.
- Ties are resolved deterministically by Foldseek record id, then original Foldseek record index.
- Record all Foldseek alternatives with lengths and hashes.
- Do not use labels, EC, names, mechanism prose, expert notes, or model outcomes to choose chains.
- Pair Foldseek-emitted amino acid tokens with aligned Foldseek 3Di tokens lowercased for SaProt input.
- Whole-sequence/whole-structure mean pooling is the primary representation; active-site pooling remains a future ablation.

## Coverage

- Foldseek emitted 1,833 records across 672 staged coordinate files.
- 661 of 702 current rows are SaProt-token compatible.
- 41 rows are blocked before SaProt embedding:
  - 34 in-distribution
  - 7 held out
- The 41 blockers include the prior missing/un-staged selected coordinates plus model-token compatibility blockers:
  - 6 selected records exceed the HF model 1,024-residue limit.
  - 9 selected records contain unsupported Foldseek amino-acid token `X`.
- 414 rows had multiple Foldseek records; all alternatives are recorded, and longest-record selection was applied deterministically.

## Backend

- Model: `westlake-repl/SaProt_35M_AF2`
- Revision/SHA: `316cd4017d29f4657b959365f24b57f1ee278912`
- Embedding dimension: 480
- Pooling: mean last hidden state over non-special whole-sequence SA tokens
- Python: `/opt/homebrew/Caskroom/miniconda/base/bin/python`
- `torch`: 2.7.1
- `transformers`: 4.53.2
- `huggingface_hub`: 0.33.4
- Cache path: `/private/tmp/catalytic-saprot-hf-cache`
- Recorded cache size in metrics artifact: 766,366,756 bytes
- Recorded main weight size: `pytorch_model.bin` 136,862,061 bytes
- Foldseek: `/private/tmp/catalytic-foldseek-env/bin/foldseek`, version `718d42176d2f67d36a60866fedfb881f8d5a7ebf`

## Metrics

From `saprot_metrics_current702_20260525.json`:

- Primary macro-F1: 0.5134
- Primary supervised accuracy: 0.3333, 15/45
- Exact label accuracy, all heldout: 0.6357
- Exact label accuracy, in-scope heldout: 0.3125
- OOS false-positive rate without threshold: 0.1957, 18/92
- Embedded heldout rows: 133
- Heldout coordinate/tokenization abstentions: 7

Per-fingerprint top-1 accuracy:

- `flavin_dehydrogenase_reductase`: 0.4000, 4/10
- `heme_peroxidase_oxidase`: 0.5000, 2/4, underpowered
- `metal_dependent_hydrolase`: 0.0588, 1/17
- `plp_dependent_enzyme`: 0.8333, 5/6
- `ser_his_acid_hydrolase`: 0.3750, 3/8

OOS diagnostics by tier:

- `far_oos`: false-positive rate 0.0000, abstention rate 1.0000, 1 row
- `near_oos`: false-positive rate 0.3333, abstention rate 0.6667, 3 rows
- `unknown_oos`: false-positive rate 0.1932, abstention rate 0.8068, 88 rows

Comparator context:

- Sequence-NN current702 primary accuracy was 0.1556 and OOS FP rate was 0.2717; bounded SaProt-35M is +0.1777 primary accuracy with lower OOS FP rate.
- Foldseek 3Di current702 is represented here as tokenization coverage, not a predictive metric.
- ProtT5 current702 comparator is not available in this branch.
- ESM-2 150M exists only as the prior 12-row external-source sample artifact, not a current702 direct comparator.

## Verification

- JSON artifacts validated with `python -m json.tool`.
- JSONL artifacts parsed successfully:
  - 661 token rows
  - 140 heldout prediction rows
- `PYTHONPATH=src python -m catalytic_earth.cli validate` passed:
  - 12 source records
  - 8 mechanism fingerprints
  - 15 mechanism ontology families
  - 702 curated mechanism labels

## Caveats

- No labels, fingerprints, ontology, production scoring, thresholds, or main docs were edited.
- No large model was trained.
- No EC/name/prose/expert-note fields were used as predictive features.
- SaProt-650M remains uncomputed.
- The nearest-neighbor classifier has no calibrated abstention threshold; abstention is only nearest-train out-of-scope or explicit coordinate/tokenization blocker.
